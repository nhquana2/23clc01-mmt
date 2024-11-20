import socket
from threading import Thread
import time
import globals
config = globals.config

from .handle import *

from globals.logger import *

def create_server(host, port):
    """Creates a server socket."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        return server
    except socket.error as e:
        logger.info("Socket error: ", e)
        return None
    except Exception as e:
        logger.info("General error: ", e)
        return None

def accept_incoming_connections(server, clients, buffer_size, encoding):
    while True:
        client, client_address = server.accept()
        logger.info("(%s:%s) has connected to the server." % client_address)
        #client.send(bytes("Please enter your name: ", encoding))
        clientThread = Thread(target=handle_client, args=(client, client_address, buffer_size, clients, encoding))
        clientThread.daemon = True
        clientThread.start()
