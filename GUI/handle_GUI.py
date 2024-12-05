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
import os


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
    path = path_label.cget("text")
    if not path or path == "No file selected":
        progress_label.configure(text="Please select a valid file or directory.", text_color = "Red")
        return
    progress_label.configure(text=f"Uploading file to {server_ip}:{server_port}...", text_color = "Red")
    if not server_ip or not validate_ip(server_ip):
        progress_label.configure(text="Invalid IP address. Please enter a valid IP.", text_color = "Red")
        return

    if not server_port or not validate_port(server_port):
        progress_label.configure(text="Invalid port. Please enter a valid port (1-65535).", text_color = "Red")
        return
    try:
      signal.signal(signal.SIGINT, handle_sigint)
      msg = [""]
      handle_upload_command(path,server_ip,int(server_port), msg, config.KEY)
    except Exception as e:
       progress_label.configure(text=f"Upload failed: {str(e)}", text_color = "Red")
    progress_label.configure(text= msg[0], text_color = "white")

def handle_download(path_label, progress_label, upper_frame):
    server_ip = upper_frame.get_ip()
    server_port = upper_frame.get_port()
    
    path = path_label.get()
    if not path or path == "No file selected":
        progress_label.configure(text="Please select a valid file or directory.", text_color = "Red")
        return
    if not server_ip or not validate_ip(server_ip):
        progress_label.configure(text="Invalid IP address. Please enter a valid IP.", text_color = "Red")
        return

    if not server_port or not validate_port(server_port):
        progress_label.configure(text="Invalid port. Please enter a valid port (1-65535).", text_color = "Red")
        return
   

    script_directory = os.path.dirname(os.path.abspath(__file__))
    script_directory = os.path.dirname(script_directory)
    server_directory = os.path.abspath(os.path.join(script_directory, "server_files"))
    file_path = os.path.join(server_directory, path)
    try:
        msg = [""]
        if not os.path.commonpath([server_directory]) == os.path.commonpath([server_directory, file_path]):
            msg[0] = ("Invalid file name or path traversal detected.")

        if not os.path.exists(file_path):
            msg[0] = (f"File '{path}' does not exist on the server.")

        signal.signal(signal.SIGINT, handle_sigint)
        
        handle_download_command(file_path,server_ip,int(server_port), msg, config.KEY)
    except Exception as e:
       progress_label.configure(text=f"Download failed: {str(e)}", text_color = "Red")
    progress_label.configure(text= msg[0], text_color = "white", wraplength = upper_frame.winfo_width()- 50)
    