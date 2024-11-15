import globals
config = globals.config
import time
import os
from threading import Thread
from server_modules.connection import create_server
import logging

logging.basicConfig(level=logging.INFO)
UPLOAD_FOLDER=config.UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def handle_client(client_socket, client_address, buffer_size, encoding):
    logging.info(f"[+] Client {client_address} connected.")
    try:
        while True:
            command = client_socket.recv(buffer_size).decode(encoding)
            if command == 'UPLOAD':
                filename = client_socket.recv(buffer_size).decode(encoding)
                file_size = int(client_socket.recv(buffer_size).decode(encoding))
                file_path = os.path.join(UPLOAD_FOLDER, filename) 
                
                with open(file_path, "wb") as f:
                    bytes_read = 0
                    while bytes_read < file_size:
                        data = client_socket.recv(min(buffer_size, file_size - bytes_read))
                        if not data:
                            break
                        f.write(data)
                        bytes_read += len(data)
                logging.info(f"[+] Received file {filename} from {client_address} and saved to {UPLOAD_FOLDER}.")
                client_socket.send(f"File {filename} uploaded successfully.".encode(encoding))

            elif command == 'DOWNLOAD':
                filename = client_socket.recv(buffer_size).decode(encoding)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    client_socket.send(str(file_size).encode(encoding))
                    with open(file_path, "rb") as f:
                        while (data := f.read(buffer_size)):
                            client_socket.sendall(data)
                    logging.info(f"[+] Sent file {filename} to {client_address}.")
                else:
                    client_socket.send("FILE NOT FOUND".encode(encoding))
            
            elif command == 'EXIT':
                logging.info(f"[-] Client {client_address} disconnected.")
                break
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def accept_incoming_connections(server_socket, clients, buffer_size, encoding):
    while True:
        client_socket, client_address = server_socket.accept()
        clients[client_address] = client_socket
        client_thread = Thread(target=handle_client, args=(client_socket, client_address, buffer_size, encoding))
        client_thread.daemon = True
        client_thread.start()

def main():
    CLIENTS = {}
    SERVER = create_server(config.SERVER_HOST, config.SERVER_PORT)
    if SERVER is None:
        print("Server could not be created. Program terminated.")
        return
    logging.info("Server is running on %s:%s" % (config.SERVER_HOST, config.SERVER_PORT))
    try:
        ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER, CLIENTS, config.BUFFER_SIZE, config.ENCODING))
        ACCEPT_THREAD.daemon = True
        ACCEPT_THREAD.start()
        input("Press Enter to shut down the server...\n")
    except KeyboardInterrupt:
        logging.info("Server shutdown requested.")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        SERVER.close()
        logging.info("Server closed.")

if __name__ == "__main__":
    main()
