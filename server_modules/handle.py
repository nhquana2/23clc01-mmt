import socket
from .utilities import *
from globals.utils import *
from threading import Thread
from alive_progress import *
from globals.logger import *

UPLOAD_FOLDER=config.UPLOAD_FOLDER

from globals.utils import *

"""Handles a single client connection."""
def handle_client(client_socket, client_address, buffer_size, encoding):
    logger.info(f"[+] Client {client_address} connected.")
    try:
        while True:
            # print("before command recv")
            command = recv_data(client_socket).decode(encoding)
            if command == 'UPLOAD':
                filename = recv_data(client_socket).decode(encoding)
                file_size = int(recv_data(client_socket).decode(encoding))
                file_path = os.path.join(UPLOAD_FOLDER, filename) 
                
                with open(file_path, "wb") as f:
                    bytes_read = 0
                    with alive_bar(file_size, title=f"Receiving {filename}") as bar:
                        while bytes_read < file_size:
                            data = recv_data(client_socket)
                            if not data:
                                break
                            f.write(data)
                            bytes_read += len(data)
                            bar(len(data))
                logger.info(f"[+] Received file {filename} from {client_address} and saved to {UPLOAD_FOLDER}.")
                #client_socket.send(f"File {filename} uploaded successfully.".encode(encoding))
                send_data(client_socket, f"File {filename} uploaded successfully.".encode(encoding))

            elif command == 'DOWNLOAD':
                filename = recv_data(client_socket).decode(encoding)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    send_data(client_socket, str(file_size).encode(encoding))
                    with open(file_path, "rb") as f:
                        with alive_bar(file_size, title=f"Sending {filename}") as bar:
                            while (data := f.read(buffer_size)):
                                send_data(client_socket, data)
                                bar(len(data))
                    logger.info(f"[+] Sent file {filename} to {client_address}.")
                else:
                    send_data(client_socket, "FILE NOT FOUND".encode(encoding))
            
            elif command == 'EXIT':
                logger.info(f"[-] Client {client_address} disconnected.")
                break
    except Exception as e:
        logger.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        
        
def accept_incoming_connections(server_socket, clients, buffer_size, encoding):
    while True:
        client_socket, client_address = server_socket.accept()
        clients[client_address] = client_socket
        client_thread = Thread(target=handle_client, args=(client_socket, client_address, buffer_size, encoding))
        client_thread.daemon = True
        client_thread.start()
