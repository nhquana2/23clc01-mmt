#Universal utility functions used by both the client and server

from .logger import *
from . import config

"""
send_data: Sends ALL data (with message boundaries) to the client or server.
Parameters:
    conn: The connection object.
    data: The data to send.
"""

def send_data(conn, data):
    data_len = len(data)
    header = data_len.to_bytes(config.HEADER_SIZE, byteorder='big')
    conn.sendall(header + data) 

"""
recv_data: Receives ALL data (with message boundaries) from the client or server.
Parameters:
    conn: The connection object.
Returns:
    The received data (all data sent by the client in ONE send_data call above).
"""

def recv_data(conn):
    conn.settimeout(5.0)
    header_chunks = []
    header_bytes_recd = 0
    while header_bytes_recd < config.HEADER_SIZE:
        chunk = conn.recv(min(config.HEADER_SIZE - header_bytes_recd, config.BUFFER_SIZE))
        if not chunk:
            raise Exception("Header receive error. Maybe the connection was closed.")
        header_chunks.append(chunk)
        header_bytes_recd += len(chunk)
    
    header = b''.join(header_chunks)
    data_len = int.from_bytes(header[0:config.HEADER_SIZE], byteorder='big')

    chunks = []
    bytes_recd = 0

    while bytes_recd < data_len:
        chunk = conn.recv(min(data_len - bytes_recd, config.BUFFER_SIZE))
        if not chunk:
            raise Exception("Chunk receive error. Maybe the connection was closed.")
        chunks.append(chunk)
        bytes_recd += len(chunk)

    return b''.join(chunks)
