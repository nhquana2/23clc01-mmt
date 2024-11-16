import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
from globals.utils import *
import socket
import os
from threading import Thread

from globals.utils import *

SERVER_HOST=config.SERVER_HOST
SERVER_PORT=config.SERVER_PORT
BUFFER_SIZE=config.BUFFER_SIZE
ENCODING=config.ENCODING

def upload_file(filename, client_socket):
    if not os.path.exists(filename):
        print(f"File '{filename}' not found!")
        return
    try:
        send_data(client_socket, "UPLOAD".encode(ENCODING))
        send_data(client_socket, filename.encode(ENCODING))
        file_size = os.path.getsize(filename)
        send_data(client_socket, str(file_size).encode(ENCODING))

        with open(filename, "rb") as f:
            bytes_sent = 0
            while bytes_sent < file_size:
                data = f.read(BUFFER_SIZE)
                send_data(client_socket, data)
                bytes_sent += len(data)
        response = recv_data(client_socket).decode(ENCODING)
        print(f"\n[+] {response}")
    except Exception as e:
        print(f"An error occurred during file upload: {e}")

def download_file(filename, client_socket):
    try:
        send_data(client_socket, "DOWNLOAD".encode(ENCODING))
        send_data(client_socket, filename.encode(ENCODING))
        response = recv_data(client_socket).decode(ENCODING)
        if response == "FILE NOT FOUND":
            print(f"File '{filename}' not found on server.")
        else:
            file_size = int(response)
            with open(f"downloaded_{filename}", "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    data = recv_data(client_socket)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)
            #print(f"File '{filename}' downloaded successfully.")
    except Exception as e:
        print(f"An error occurred during file download: {e}")
        
def handle_command(command, conn):
    if command.startswith("upload "):
        filename = command[7:].strip()
        upload_thread = Thread(target=upload_file, args=(filename, conn), daemon=True)
        upload_thread.start()
    elif command.startswith("download "):
        filename = command[9:].strip()
        download_thread = Thread(target=download_file, args=(filename, conn), daemon=True)
        download_thread.start()
    else:
        print("Invalid command. Use 'upload <filename>' or 'download <filename>'.")
