import globals
config = globals.config
utils = globals.utils
import time
from client_modules.connection import *
from client_modules.handle import *
from globals.utils import *
import socket
import os
from threading import Thread

from globals.logger import *
from globals.console import console

def main():
    while True:
           handle_command()

if __name__ == "__main__":
    main()
