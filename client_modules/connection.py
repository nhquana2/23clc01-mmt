import socket

"""Connects to a server socket."""
def connect_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)
    client.connect((host, port))
    return client