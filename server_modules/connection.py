from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import globals
config = globals.config

def create_server(host, port):
    """Creates a server socket."""
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    return server

def broadcast(msg, clients, prefix=""): 
    """Broadcasts a message to all the clients."""
    #print(clients)
    #print("ok")
    for sock in clients.values():
        sock.send(bytes(prefix, "utf8")+msg)


def handle_client(client, client_address, buffer_size, clients, encoding):
    """Handles a single client connection."""
    name = client.recv(buffer_size).decode(encoding)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, encoding))
    msg = "%s đã tham gia kết nối!" % name
    broadcast(bytes(msg, encoding), clients)
    #clients[client] = name
    clients[client_address] = client

    while True:
        msg = client.recv(buffer_size)
        if msg != bytes("{quit}", encoding):
            broadcast(msg, clients, name+": ")
        else:
            client.send(bytes("{quit}", encoding))
            client.close()
            del clients[client_address]
            broadcast(bytes("%s đã đóng kết nối." % name, encoding))
            break

def accept_incoming_connections(server, clients, buffer_size, encoding):
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Client ơi vui lòng nhập tên: ", encoding))
        clientThread = Thread(target=handle_client, args=(client, client_address, buffer_size, clients, encoding))
        clientThread.daemon = True
        clientThread.start()
