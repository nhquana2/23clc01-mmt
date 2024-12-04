import socket
from globals.utils import *
from threading import Thread
from globals.logger import *
import time
from client_modules.handle import *
UPLOAD_FOLDER=config.UPLOAD_FOLDER
import platform
import re
from globals.utils import *



def validate_ip(ip):
    ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ip_pattern, ip) is not None

def validate_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False
    
def handle_upload(server_ip, server_port, path_label, progress_label):
    print(f"{server_ip} {server_port}")
    path = path_label.cget("text")
    if not path or path == "No file selected":
        progress_label.configure(text="Please select a valid file or directory.")
        return
    progress_label.configure(text=f"Uploading file to {server_ip}:{server_port}...")
    if not server_ip or not validate_ip(server_ip):
        progress_label.configure(text="Invalid IP address. Please enter a valid IP.")
        return

    if not server_port or not validate_port(server_port):
        progress_label.configure(text="Invalid port. Please enter a valid port (1-65535).")
        return
    try:
      # print(f"{path} {server_ip} {server_port}")
      signal.signal(signal.SIGINT, handle_sigint)
      if server_port == config.SERVER_PORT:
          print("ye")
      if  (server_ip) == config.SERVER_PORT:
          print("yew2")
      server_ip = config.SERVER_HOST
      server_port = config . SERVER_PORT
      handle_upload_command(path,server_ip,server_port)
    except Exception as e:
       progress_label.configure(text=f"Upload failed: {str(e)}")

    progress_label.configure(text="Upload successful.")

   
    