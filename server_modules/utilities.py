import os
import json

def retrieve_file_request(client):
    """Retrieves a file request from the client."""
    data = client.recv(1024).decode("utf8").strip()
    if data.startswith("upload"):
        return "upload", data[6:]
    elif data.startswith("download"):
        return "download", data[8:]
    else:
        return None, None

def load_valid_keys(key_file):
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return json.load(f)
    return []

def is_valid_key(keyVal, valid_keys):
    return keyVal in valid_keys