import logging

#logger configuration
FMT = "[{levelname}] {name}: {asctime} | {filename}:{lineno} | {process} >>> {message}"
FORMATS = {
    logging.DEBUG: FMT,
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m"
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style = "{")
        return formatter.format(record)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')
console_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(logging.Formatter(FMT, style = "{"))

logging.basicConfig(
    level = logging.DEBUG,
    handlers = [console_handler, file_handler]
)

logger = logging.getLogger("socket_app")