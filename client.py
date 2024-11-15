import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
from globals.utils import *
import socket
import os
from threading import Thread


SERVER_HOST=config.SERVER_HOST
SERVER_PORT=config.SERVER_PORT
BUFFER_SIZE=config.BUFFER_SIZE
ENCODING=config.ENCODING

# Kết nối tới server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def upload_file(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' not found!")
        return
    try:
        client_socket.send("UPLOAD".encode(ENCODING))
        client_socket.send(filename.encode(ENCODING))
        file_size = os.path.getsize(filename)
        client_socket.send(str(file_size).encode(ENCODING))

        with open(filename, "rb") as f:
            bytes_sent = 0
            while bytes_sent < file_size:
                data = f.read(BUFFER_SIZE)
                client_socket.sendall(data)
                bytes_sent += len(data)
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODING)
        print(f"\n[+] {response}")
    except Exception as e:
        print(f"An error occurred during file upload: {e}")

def download_file(filename):
    try:
        client_socket.send("DOWNLOAD".encode(ENCODING))
        client_socket.send(filename.encode(ENCODING))
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODING)
        if response == "FILE NOT FOUND":
            print(f"File '{filename}' not found on server.")
        else:
            file_size = int(response)
            with open(f"downloaded_{filename}", "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)
            print(f"File '{filename}' downloaded successfully.")
    except Exception as e:
        print(f"An error occurred during file download: {e}")

def handle_command(command):
    if command.startswith("upload "):
        filename = command[7:].strip()
        upload_thread = Thread(target=upload_file, args=(filename,), daemon=True)
        upload_thread.start()
    elif command.startswith("download "):
        filename = command[9:].strip()
        download_thread = Thread(target=download_file, args=(filename,), daemon=True)
        download_thread.start()
    else:
        print("Invalid command. Use 'upload <filename>' or 'download <filename>'.")

def main():
    while True:
        command = input("Enter command (upload <filename> or download <filename>): ").strip()
        if command == "exit":
            client_socket.send("EXIT".encode(ENCODING))
            print("Disconnected from server.")
            break
        else:
            handle_command(command)

    client_socket.close()

if __name__ == "__main__":
    main()
