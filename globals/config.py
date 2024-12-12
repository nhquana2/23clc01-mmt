from dotenv import dotenv_values
from .logger import *

"""
init_env_values: Initializes the global variables with the values from the .env file.
"""

def init_env_values():
    try:
        env_values = dotenv_values(".env")
        global KEY, SERVER_HOST, SERVER_PORT, CLIENT_HOST, BUFFER_SIZE, ENCODING, HEADER_SIZE, UPLOAD_FOLDER
        SERVER_HOST = env_values["SERVER_HOST"]
        SERVER_PORT = int(env_values["SERVER_PORT"])
        CLIENT_HOST = env_values["CLIENT_HOST"]
        BUFFER_SIZE = int(env_values["BUFFER_SIZE"])
        HEADER_SIZE = int(env_values["HEADER_SIZE"])
        ENCODING = env_values["ENCODING"]
        UPLOAD_FOLDER = env_values["UPLOAD_FOLDER"]
        KEY = env_values["KEY"]
        logger.info("Environment variables loaded into global variables.")
    except Exception as e:
        logger.error(f"Error loading environment variables: {e}")
        exit(1)