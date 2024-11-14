import globals
config = globals.config
import time
from server_modules.connection import *

import logging
logging.basicConfig(level = logging.INFO)

def main():
    CLIENTS = {}
    SERVER = create_server(config.SERVER_HOST, config.SERVER_PORT)
    if (SERVER == None):
        print("Server could not be created. Program terminated.")
        return
    logging.info("Server is running on %s:%s" % (config.SERVER_HOST, config.SERVER_PORT))
    try: 
        ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER, CLIENTS, config.BUFFER_SIZE, config.ENCODING))
        ACCEPT_THREAD.daemon = True
        ACCEPT_THREAD.start()
        input()
    except KeyboardInterrupt:
        SERVER.close()
    except Exception as e:
        SERVER.close()
        print("Error: ", e)
    finally:
        print("Server closed.")

if __name__ == "__main__":
    main()