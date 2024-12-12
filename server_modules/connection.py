import socket
from threading import Thread
import globals
config = globals.config

from .handle import *

from globals.logger import *

"""
create_server: Creates a server socket.
Parameters:
    host: The host IP address.
    port: The port number.
Returns:
    The server socket (None if error occured).
"""

def create_server(host, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)

        if not os.path.exists(config.UPLOAD_FOLDER):
            os.makedirs(config.UPLOAD_FOLDER)

        return server
    except socket.error as e:
        logger.info("Socket error: %s" % e)
        return None
    except Exception as e:
        logger.info("General error: %s" % e)
        return None

"""
accept_incoming_connections: Accepts incoming connections from clients.
Parameters:
    server: The server socket.
    clients: The dictionary of clients (used for managing if needed).
    buffer_size: The buffer size.
    encoding: The encoding.
"""

def accept_incoming_connections(server_socket, clients, buffer_size, encoding):
    while True:
        client_socket, client_address = server_socket.accept()
        clients[client_address] = client_socket
        client_thread = Thread(target=handle_client, args=(client_socket, client_address, buffer_size, encoding))
        client_thread.daemon = True
        client_thread.start()
