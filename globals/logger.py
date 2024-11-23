import logging
from rich.logging import RichHandler

#logger configuration
FORMAT = "%(message)s"
FMT = "[{levelname}] {name}: {asctime} | {filename}:{lineno} | {process} >>> {message}"

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter(FMT, style = "{"))

logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]",
    handlers = [RichHandler(rich_tracebacks=True), file_handler]
)

logger = logging.getLogger("socket_app")