import globals
config = globals.config
utils = globals.utils
import time
import signal
from client_modules.connection import *
import socket
import os

from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event

from globals.utils import *
from globals.console import console

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

SERVER_HOST=config.SERVER_HOST
SERVER_PORT=config.SERVER_PORT
BUFFER_SIZE=config.BUFFER_SIZE
ENCODING=config.ENCODING

def upload_file(file_path, task_id, progress) -> None:

    if not os.path.exists(file_path):
        progress.console.print(f"Path '{file_path}' not found!")
        return
    try:
        client_socket = connect_server(config.SERVER_HOST, config.SERVER_PORT)
        if client_socket is None:
            progress.console.print("[bold red]Server could not be connected. Program terminated.")
            return
        client_ip, client_port = client_socket.getsockname()
        logger.info("Client ('%s':%s) is connected to server ('%s':%s)" % (client_ip, client_port, config.SERVER_HOST, config.SERVER_PORT))

        file_name = os.path.basename(file_path)

        send_data(client_socket, "UPLOAD".encode(ENCODING))
        send_data(client_socket, file_name.encode(ENCODING))
        file_size = os.path.getsize(file_path)
        send_data(client_socket, str(file_size).encode(ENCODING))

        progress.update(task_id, total=file_size)

        with open(file_path, "rb") as f:
            bytes_sent = 0
            progress.start_task(task_id)
            while bytes_sent < file_size:
                data = f.read(BUFFER_SIZE)
                send_data(client_socket, data)
                bytes_sent += len(data)
                progress.update(task_id, advance=len(data))
        response = recv_data(client_socket).decode(ENCODING)
        progress.console.print(f"[+] {response}")
    except Exception as e:
        progress.console.print(f"An error occurred during file upload: {e}")
    finally:
        client_socket.close()

def download_file(file_name, task_id, progress) -> None:
    try:
        client_socket = connect_server(config.SERVER_HOST, config.SERVER_PORT)
        if client_socket is None:
            progress.console.print("[bold red]Server could not be connected. Program terminated.")
            return
        client_ip, client_port = client_socket.getsockname()
        logger.info("Client ('%s':%s) is connected to server ('%s':%s)" % (client_ip, client_port, config.SERVER_HOST, config.SERVER_PORT))    
        send_data(client_socket, "DOWNLOAD".encode(ENCODING))
        send_data(client_socket, file_name.encode(ENCODING))
        response = recv_data(client_socket).decode(ENCODING)
        if response == "FILE NOT FOUND":
            progress.console.print(f"File '{file_name}' not found on server.")
        else:
            file_size = int(response)
            progress.update(task_id, total=file_size)

            with open(f"downloaded_{file_name}", "wb") as f:
                bytes_received = 0
                progress.start_task(task_id)
                while bytes_received < file_size:
                    data = recv_data(client_socket)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)
                    progress.update(task_id, advance=len(data))
            progress.console.print(f"File '{file_name}' downloaded successfully.")
    except Exception as e:
        progress.console.print(f"An error occurred during file download: {e}")
    finally:
        client_socket.close()

def handle_download_command(file_name):
    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )
    with progress:
        with ThreadPoolExecutor() as pool:
            task_id = progress.add_task("Download", filename=file_name, start=False)
            pool.submit(download_file, file_name, task_id, progress)

def handle_upload_command(path):
    file_paths = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_paths.append(os.path.join(root, file))
    else:
        file_paths.append(path)

    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )    

    with progress:
        with ThreadPoolExecutor() as pool:
            for file_path in file_paths:
                task_id = progress.add_task("Upload", filename=os.path.basename(file_path), start=False)
                pool.submit(upload_file, file_path, task_id, progress)

def handle_command():
    command = console.input("Enter command (upload <file_path> or download <file_name> or exit): ").strip()
    if command == "exit":
            console.print("Disconnected from server.")
            return
    if command.startswith("upload "):
        path = command[7:].strip()
        handle_upload_command(path)
    elif command.startswith("download "):
        path = command[9:].strip()
        handle_download_command(path)
        
    else:
        console.print("Invalid command. Use 'upload <file_path>' or 'download <file_name> or exit'.")
