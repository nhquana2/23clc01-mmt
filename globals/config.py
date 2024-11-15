from dotenv import dotenv_values
import logging
logging.basicConfig(level = logging.INFO)

# Get the values from the .env file and set them as global variables
def init_env_values():
    env_values = dotenv_values(".env")
    global SERVER_HOST, SERVER_PORT, CLIENT_HOST, BUFFER_SIZE, ENCODING, HEADER_SIZE, UPLOAD_FOLDER
    SERVER_HOST = env_values["SERVER_HOST"]
    SERVER_PORT = int(env_values["SERVER_PORT"])
    CLIENT_HOST = env_values["CLIENT_HOST"]
    BUFFER_SIZE = int(env_values["BUFFER_SIZE"])
    HEADER_SIZE = int(env_values["HEADER_SIZE"])
    ENCODING = env_values["ENCODING"]
    UPLOAD_FOLDER = env_values["UPLOAD_FOLDER"]
    logging.info("Environment variables loaded into global variables.")