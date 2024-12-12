import os
import json

def load_valid_keys(key_file):
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return json.load(f)
    return []

def is_valid_key(keyVal, valid_keys):
    return keyVal in valid_keys