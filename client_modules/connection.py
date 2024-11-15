import socket
from threading import Thread
import time
import globals
config = globals.config

import logging
logging.basicConfig(level = logging.INFO)

"""Connects to a server socket."""
def connect_server(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        return client
    except socket.error as e:
        logging.error("Socket error: %s", e)
        return None
    except Exception as e:
        logging.error("General error: %s", e)
        return None