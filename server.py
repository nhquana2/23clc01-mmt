import globals
config = globals.config
import time
from server_modules.connection import *

def main():
    CLIENTS = {}
    SERVER = create_server(config.SERVER_HOST, config.SERVER_PORT)
    SERVER.listen(5)
    print("Waiting for connection...")
    try: 
        ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(SERVER, CLIENTS, config.BUFFER_SIZE, config.ENCODING))
        ACCEPT_THREAD.daemon = True
        ACCEPT_THREAD.start()
    except Exception as e:
        SERVER.close()
        print("Error: ", e)
    
    input("Input to close server.")
    print("Server shutted down.")

if __name__ == "__main__":
    main()