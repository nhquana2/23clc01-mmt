import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *

import logging
logging.basicConfig(level = logging.INFO)

def main():

    CLIENT = connect_server(config.SERVER_HOST, config.SERVER_PORT)
    if (CLIENT == None):
        print("Client could not connect to the server. Program terminated.")
        return
    logging.info("Client is connected to %s:%s" % (config.SERVER_HOST, config.SERVER_PORT))

    """while True:
        #command 1: upload <file_path>
        #command 2: download <file_path>
        #command 3: exit
        command = input()
        command_args = command.split(" ")
        if command_args[0] == "upload":
            upload_file(CLIENT, command_args[1])
        elif command_args[0] == "download":
            download_file(CLIENT, command_args[1])
        elif command_args[0] == "exit":
            break
        else:
            print("Invalid command. Please try again.")

    CLIENT.close()"""

if __name__ == "__main__":
    main()