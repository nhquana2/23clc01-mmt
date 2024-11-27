import globals
config = globals.config
import time
import os
from threading import Thread
from server_modules.connection import *
from server_modules.handle import *

from globals.utils import *
from globals.logger import *

from globals.console import console

def main():
    CLIENTS = {}
    SERVER = create_server(config.SERVER_HOST, config.SERVER_PORT)
    if SERVER is None:
        console.print("Server could not be created. Program terminated.", style="bold red")
        return
    logger.info("Server is running on %s:%s" % (config.SERVER_HOST, config.SERVER_PORT))
    try:
        ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER, CLIENTS, config.BUFFER_SIZE, config.ENCODING))
        ACCEPT_THREAD.daemon = True
        ACCEPT_THREAD.start()
        input("Enter anything or send Ctrl-C to shut down the server...\n")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested.")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        SERVER.close()
        logger.info("Server closed.")

if __name__ == "__main__":
    main()
