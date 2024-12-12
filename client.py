import globals
config = globals.config
utils = globals.utils
from client_modules.connection import *
from client_modules.handle import *
from globals.utils import *

from globals.logger import *
from globals.console import console

#Entry point for the client CLI program

def main():
    try:
        config.KEY = console.input("Enter your authentication key: ")
        while True:
            handle_command()
    except KeyboardInterrupt:
        console.print("\nClient program terminated.",style="blue")
    except Exception as e:
        console.print(f"\nError occured: {e}", style="bold red")

if __name__ == "__main__":
    main()
