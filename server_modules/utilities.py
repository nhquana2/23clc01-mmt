import os

def retrieve_file_request(client):
    """Retrieves a file request from the client."""
    data = client.recv(1024).decode("utf8").strip()
    if data.startswith("upload"):
        return "upload", data[6:]
    elif data.startswith("download"):
        return "download", data[8:]
    else:
        return None, None
