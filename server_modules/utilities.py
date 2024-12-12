import os
import json
import time

def load_valid_keys(key_file):
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return json.load(f)
    return []

def is_valid_key(keyVal, valid_keys):
    return keyVal in valid_keys

def generate_unique_filename(file_path):
    if not os.path.exists(file_path):
        return file_path
    
    base, ext = os.path.splitext(file_path)
    timestamp = int(time.time() * 1000) 
    new_file_path = f"{base}_{timestamp}{ext}"
    
    return new_file_path