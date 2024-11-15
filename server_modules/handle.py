import socket
from .utilities import *

import logging
logging.basicConfig(level = logging.INFO)

"""Handles a single client connection."""
def handle_client(client, client_address, buffer_size, clients, encoding):
    try:
        clients[client_address] = client
        request_type, file_info = retrieve_file_request(client)
        if not request_type or not file_info:
            raise ValueError("Request type or file path is invalid.")
        logging.info("(%s:%s) send an %s request with file info %s" % (client_address[0], client_address[1], request_type, file_info))
    except socket.error as e:
        logging.error("Socket error: %s", e)
    except ValueError as e:
        logging.error("Value error: %s", e)
    except OSError as e:
        logging.error("OS error: %s", e)
    except Exception as e:
        logging.error("General error: %s", e)
    finally:
        client.close()
        del clients[client_address]