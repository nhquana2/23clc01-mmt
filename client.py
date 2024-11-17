import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
import client_modules.handle
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



def main():
    while True:
           client_modules.handle.handle_command(client_socket)

    client_socket.close()

if __name__ == "__main__":
    main()
