from .utilities import *



"""Handles a single client connection."""
def handle_client(client, client_address, buffer_size, clients, encoding):
    try:
        request_type, file_info = retrieve_file_request(client)
        if not request_type or not file_info:
            raise AttributeError("Request type or file path is invalid.")
        logging.info("(%s:%s) send an %s request with file info %sq " % (client_address[0], client_address[1], request_type, file_info))
    except socket.error as e:
        logging.info("Socket error: ", e)
    except AttributeError as e:
        logging.info("Attribute error: ", e)
    except OSError as e:
        logging.info("File/ OS error: ", e)
    except Exception as e:
        logging.info("General error: ", e)
    finally:
        client.close()
        del clients[client_address]