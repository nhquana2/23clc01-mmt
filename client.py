import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
from client_modules.handle import *
from globals.utils import *
import socket
import os
from threading import Thread

from globals.logger import *

def main():
    client_socket = connect_server(config.SERVER_HOST, config.SERVER_PORT)
    if client_socket is None:
        print("Server could not be connected. Program terminated.")
        return

    client_ip, client_port = client_socket.getsockname()
    logger.info("Client ('%s':%s) is connected to server ('%s':%s)" % (client_ip, client_port, config.SERVER_HOST, config.SERVER_PORT))

    while True:
           handle_command(client_socket)
    client_socket.close()

if __name__ == "__main__":
    main()
