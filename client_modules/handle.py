import os
import signal

import globals
config = globals.config
utils = globals.utils

from globals.utils import *
from globals.console import console

from client_modules.connection import *

from concurrent.futures import ThreadPoolExecutor
from threading import Event


from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

SERVER_HOST=config.SERVER_HOST
SERVER_PORT=config.SERVER_PORT
BUFFER_SIZE=config.BUFFER_SIZE
ENCODING=config.ENCODING

"""
done_event: an event object to signal when to stop the upload/download process
handle_sigint: a signal handler to set the done_event when a SIGINT signal is received
default_sigint: a default signal handler to raise a KeyboardInterrupt exception (default behavior for SIGINT)
"""

done_event = Event()

def handle_sigint(signum, frame):
    done_event.set()

def default_sigint(signum, frame):
    raise KeyboardInterrupt


"""
upload_file: A threaded function to upload a single file to the server 
(to be called by handle_upload_command function in a thread pool)

Parameters:
    file_path: the path of the file to be uploaded
    task_id: TaskID of the progress task (for updating and managing the progress bar)
    base_path: the base path of the file to be uploaded (for uploading directories)
    progress: the progress object to update the progress bar
    server_host: the server IPv4 address
    server_port: the server port
    msg: a list to capture the message to be displayed on client's GUI feature
    key: the authentication key to connect to the server
"""

def upload_file(file_path, task_id, base_path, progress, server_host, server_port, msg, key) -> None:
    
    if not os.path.exists(file_path):
        progress.console.print(f"Path '{file_path}' not found!", style="bold red")
        msg[0] = f"Path '{file_path}' not found!"
        return
    
    try:
        client_socket = connect_server(server_host, server_port)
        if client_socket is None:
            progress.console.print("[!] Server could not be connected. Program terminated.", style="bold red")
            msg[0] ="[!] Server could not be connected."
            return

        """
        construct file_path_on_server, it is the relative path where the file will be saved on the server
        If base_path is empty, file_path_on_server will be the file name, which uploads to the server's default directory
        If base_path is not empty, file_path_on_server will be the relative path of the file from the base_path
        For example, 
        base_path = "/users/nhquan/Documents"
        file_path = "/users/nhquan/Documents/Projects/Project1/file.txt"
        base_dir = "Documents"
        file_path_on_server = "Documents/Projects/Project1/file.txt"
        """

        file_path_on_server = os.path.basename(file_path)
        if base_path != "":
            base_dir = os.path.basename(base_path) 
            file_path_on_server = os.path.relpath(file_path, base_path)
            file_path_on_server = os.path.join(base_dir, file_path_on_server)


        send_data(client_socket, key.encode(ENCODING))

        if recv_data(client_socket).decode(ENCODING) == "INVALID_KEY":
            progress.console.print("[!] Server rejected connection, invalid key provided.", style="bold red")
            msg[0] = "[!] Server rejected connection, invalid key provided."
            client_socket.close()
            return

        send_data(client_socket, "UPLOAD".encode(ENCODING))
        send_data(client_socket, file_path_on_server.encode(ENCODING))
        file_size = os.path.getsize(file_path)
        send_data(client_socket, str(file_size).encode(ENCODING))

        progress.update(task_id, total=file_size)

        
        #Read the file in chunks of size BUFFER_SIZE and send it to the server
        with open(file_path, "rb") as f:
            bytes_sent = 0
            progress.start_task(task_id)
            while bytes_sent < file_size:
                data = f.read(BUFFER_SIZE)
                send_data(client_socket, data)
                bytes_sent += len(data)
                progress.update(task_id, advance=len(data))
                response = recv_data(client_socket).decode(ENCODING)
                #Wait for the server to acknowledge the chunk sent by the client
                if response != "OK":
                    raise Exception("Server not responding correctly.")
                if done_event.is_set():
                    raise Exception("Upload interrupted by user.")
                
        response = recv_data(client_socket).decode(ENCODING)
        progress.console.print(f"[+] {response}", style="bold green")
        msg[0] = f"[+] {response}"

    except Exception as e:
        progress.console.print(f"An error occurred during file upload: {e}", style="bold red")
        msg[0] = f"An error occurred during file upload: {e}"
    finally:
        client_socket.close()

"""
download_file: A threaded function to download a single file from the server
(to be called by handle_download_command function in a thread pool)
Parameters:
    file_path: the path of the file to be downloaded
    task_id: TaskID of the progress task (for updating and managing the progress bar)
    progress: the progress object to update the progress bar
    server_host: the server IPv4 address
    server_port: the server port
    msg: a list to capture the message to be displayed on client's GUI feature
    key: the authentication key to connect to the server
"""

def download_file(file_path, task_id, progress, server_host, server_port, msg, key) -> None:

    try:
        client_socket = connect_server(server_host, server_port)
        if client_socket is None:
            progress.console.print("[!] Server could not be connected. Program terminated.", style="bold red")
            msg[0] = "[!] Server could not be connected"
            return
        client_ip, client_port = client_socket.getsockname()
        send_data(client_socket, key.encode(ENCODING))

        if recv_data(client_socket).decode(ENCODING) == "NOT VALID":
            progress.console.print("[!] Server rejected connection by valid key", style="bold red")
            msg[0] = "[!] Server rejected connection by valid key"
            client_socket.close()
            return
        else:
            send_data(client_socket, "DOWNLOAD".encode(ENCODING))
            send_data(client_socket, file_path.encode(ENCODING))
            response = recv_data(client_socket).decode(ENCODING)
            if response == "FILE NOT FOUND":
                progress.console.print(f"File '{file_path}' not found on server.", style="bold red")
                msg[0] = f"File '{file_path}' not found on server."
            else:
                file_size = int(response)
                progress.update(task_id, total=file_size)

                file_name = os.path.basename(file_path)

                os.makedirs("client_files", exist_ok=True)

                with open(f"client_files/{file_name}", "wb") as f:
                    bytes_received = 0
                    progress.start_task(task_id)
                    while bytes_received < file_size:
                        data = recv_data(client_socket)
                        if not data:
                            break
                        f.write(data)
                        bytes_received += len(data)
                        send_data(client_socket, "OK".encode(ENCODING))
                        progress.update(task_id, advance=len(data))
                progress.console.print(f"File '{file_name}' downloaded successfully.", style="bold green")
                msg[0] = f"File '{file_name}' downloaded successfully."
    except Exception as e:
        progress.console.print(f"An error occurred during file download: {e}", style="bold red")
        msg[0] = f"An error occurred during file download: {e}"
    finally:
        client_socket.close()

def handle_download_command(file_path, server_host, server_port, msg, key):
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
            task_id = progress.add_task("Download", filename=os.path.basename(file_path), start=False)
            pool.submit(download_file, file_path, task_id, progress, server_host, server_port, msg, key)

"""
handle_upload_command: Handles the upload command from the client
Parameters:
    path: the path of the file or directory to be uploaded
    server_ip: the server IPv4 address
    server_port: the server port
    msg: a list to capture the message to be displayed on client's GUI feature
    key: the authentication key to connect to the server
"""

def handle_upload_command(path, server_ip, server_port, msg, key):
    """
    If path is a directory, file_paths will contain all the files in the directory and its subdirectories
    If path is a file, file_paths will contain only the file path
    """
    file_paths = []
    base_path = "" #base_path only needed for uploading directories
    if os.path.isdir(path):
        base_path = os.path.abspath(path)
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

    #Thread pool to upload multiple files concurrently, will blocks until all uploads are completed
    with progress:
        with ThreadPoolExecutor() as pool:
            for file_path in file_paths:
                task_id = progress.add_task("Upload", filename=os.path.basename(file_path), start=False)
                pool.submit(upload_file, file_path, task_id, base_path, progress, server_ip, server_port, msg, key)

"""
handle_command: Handles the client command line interface
"""

def handle_command():
    command = console.input("Enter command (upload <path>, download <file_path>, key <value> or exit): ").strip()
    if command == "exit":
            raise KeyboardInterrupt
    if command.startswith("key "):
        config.KEY = command[4:].strip()
        console.print("Authentication key updated successfully", style="bold green")
    elif command.startswith("upload "):
        signal.signal(signal.SIGINT, handle_sigint)
        path = command[7:].strip()
        handle_upload_command(path,config.SERVER_HOST,config.SERVER_PORT,[""], config.KEY)
        signal.signal(signal.SIGINT, default_sigint)
    elif command.startswith("download "):
        signal.signal(signal.SIGINT, handle_sigint)
        path = command[9:].strip()
        handle_download_command(path,config.SERVER_HOST,config.SERVER_PORT,[""], config.KEY)
        signal.signal(signal.SIGINT, default_sigint)
    else:
        console.print("Invalid command. Use 'upload <file_path>' or 'download <file_name> or exit'.", style="bold red")
