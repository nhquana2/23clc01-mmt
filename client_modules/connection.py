import socket
from threading import Thread
import time
import globals
config = globals.config

from globals.logger import *
from globals.console import console

"""Connects to a server socket."""
def connect_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)
    client.connect((host, port))
    return client