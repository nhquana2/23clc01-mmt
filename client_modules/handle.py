import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
from globals.utils import *
import socket
import os
from threading import Thread
from alive_progress import *
from globals.utils import *

SERVER_HOST=config.SERVER_HOST
SERVER_PORT=config.SERVER_PORT
BUFFER_SIZE=config.BUFFER_SIZE
ENCODING=config.ENCODING

def upload_file(file_path, client_socket):
    if not os.path.exists(file_path):
        print(f"Path '{file_path}' not found!")
        return
    try:
        file_name = os.path.basename(file_path)
        send_data(client_socket, "UPLOAD".encode(ENCODING))
        send_data(client_socket, file_name.encode(ENCODING))
        file_size = os.path.getsize(file_path)
        send_data(client_socket, str(file_size).encode(ENCODING))

        with open(file_path, "rb") as f:
            bytes_sent = 0
            with alive_bar(file_size, title=f"Uploading {file_name}") as bar:
                while bytes_sent < file_size:
                    data = f.read(BUFFER_SIZE)
                    send_data(client_socket, data)
                    bytes_sent += len(data)
                    bar(len(data))
        response = recv_data(client_socket).decode(ENCODING)
        print(f"\n[+] {response}")
    except Exception as e:
        print(f"An error occurred during file upload: {e}")

def download_file(file_name, client_socket):
    try:
        send_data(client_socket, "DOWNLOAD".encode(ENCODING))
        send_data(client_socket, file_name.encode(ENCODING))
        response = recv_data(client_socket).decode(ENCODING)
        if response == "FILE NOT FOUND":
            print(f"File '{file_name}' not found on server.")
        else:
            file_size = int(response)
            with open(f"downloaded_{file_name}", "wb") as f:
                bytes_received = 0
                with alive_bar(file_size, title=f"Downloading {file_name}") as bar:
                    while bytes_received < file_size:
                        data = recv_data(client_socket)
                        if not data:
                            break
                        f.write(data)
                        bytes_received += len(data)
                        bar(len(data))
            print(f"File '{file_name}' downloaded successfully.")
    except Exception as e:
        print(f"An error occurred during file download: {e}")
        
def handle_command(conn):
    command = input("Enter command (upload <file_path> or download <file_name> or exit): ").strip()
    if command == "exit":
            conn.send("EXIT".encode(ENCODING))
            print("Disconnected from server.")
            return
    if command.startswith("upload "):
        filename = command[7:].strip()
        upload_thread = Thread(target=upload_file, args=(filename, conn), daemon=True)
        upload_thread.start()
        upload_thread.join()
    elif command.startswith("download "):
        filename = command[9:].strip()
        download_thread = Thread(target=download_file, args=(filename, conn), daemon=True)
        download_thread.start()
        download_thread.join()
        
    else:
        print("Invalid command. Use 'upload <file_path>' or 'download <file_name> or exit'.")
