import logging
from rich.logging import RichHandler

#FORMAT: used for the console
#FMT: used for the log file
FORMAT = "%(message)s"
FMT = "[{levelname}] {name}: {asctime} | {filename}:{lineno} | {process} >>> {message}"

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter(FMT, style = "{"))

logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]",
    handlers = [RichHandler(rich_tracebacks=True), file_handler]
)

# Create a logger object which will be used in the entire program
logger = logging.getLogger("socket_app")