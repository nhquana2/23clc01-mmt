from .utilities import *
from globals.utils import *
from threading import Thread
from globals.logger import *
UPLOAD_FOLDER=config.UPLOAD_FOLDER
keys_file = "server_credentials/keys.json"
import platform
from globals.utils import *

"""
handle_client: Handles a SINGLE client connection.
Parameters:
    client_socket: The client socket.
    client_address: The client address.
    buffer_size: The buffer size.
    encoding: The encoding.
"""


def handle_client(client_socket, client_address, buffer_size, encoding):
    key_value = recv_data(client_socket).decode(encoding)
    valid_keys = load_valid_keys(keys_file)

    if not is_valid_key(key_value, valid_keys):
        logger.info(f"[+] Client {client_address} using auth key {key_value} failed to authenticate.")
        send_data(client_socket, "INVALID_KEY".encode(encoding))
        client_socket.close()
        return
    else: 
        logger.info(f"[+] Client {client_address} using auth key {key_value} authenticated successfully.")
        send_data(client_socket, "VALID_KEY".encode(encoding))

    logger.info(f"[+] Client {client_address} connected.")

    try:
        file_name = "<undefined>"
        command = recv_data(client_socket).decode(encoding)

        if command == 'UPLOAD':

            file_name = recv_data(client_socket).decode(encoding)

            # Fix the inconsistency in file path separators between Windows and Linux
            if platform.system() == "Linux":
                file_name = file_name.replace("\\", "/")
            else:
                file_name = file_name.replace("/", "\\")

            file_size = int(recv_data(client_socket).decode(encoding))
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            file_path = generate_unique_filename(file_path)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            logger.info(f"Start receiving file {os.path.basename(file_path)} from {client_address}...")
            
            with open(file_path, "wb") as f:
                bytes_read = 0
                while bytes_read < file_size:
                    data = recv_data(client_socket)
                    if not data:
                        break
                    f.write(data)
                    bytes_read += len(data)
                    send_data(client_socket, "OK".encode(encoding))

            
            logger.info(f"[+] Received file {os.path.basename(file_path)} from {client_address} and saved to {UPLOAD_FOLDER}.")
            send_data(client_socket, f"File {os.path.basename(file_path)} uploaded successfully.".encode(encoding))

        elif command == 'DOWNLOAD':

            file_name = recv_data(client_socket).decode(encoding)
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                send_data(client_socket, str(file_size).encode(encoding))
                with open(file_path, "rb") as f:
                    while (data := f.read(buffer_size)):
                        send_data(client_socket, data)
                        response = recv_data(client_socket).decode(encoding)
                        if response != "OK":
                            raise Exception("Client not responding correctly.")
                logger.info(f"[+] Sent file {file_name} to {client_address}.")
            else:
                send_data(client_socket, "FILE NOT FOUND".encode(encoding))

    except Exception as e:
        logger.error(f"Error handling client {client_address}: {e}")
        logger.error(f"Failed to receive file {file_name} from {client_address}.")

    finally:
        logger.info(f"[-] Client {client_address} disconnected.")
        client_socket.close()