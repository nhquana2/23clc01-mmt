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
    try:
        while True:
            handle_command()
    except KeyboardInterrupt:
        console.print("\nClient program terminated.",style="blue")
    except Exception as e:
        console.print(f"\nError occured: {e}", style="bold red")

if __name__ == "__main__":
    main()
