import globals
config = globals.config
import time
import os
from threading import Thread
from server_modules.connection import create_server
import logging
import server_modules.handle
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER=config.UPLOAD_FOLDER
accept_incoming_connections = server_modules.handle.accept_incoming_connections
handle_client = server_modules.handle.handle_client


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



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
