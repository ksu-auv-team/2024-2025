from logging import getLogger, StreamHandler, Formatter, DEBUG
import os
from logging import FileHandler
from datetime import datetime

class Logger:
    def __init__(self, name: str, print_debug: bool):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)

        # Formatter for both handlers
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create logs directory inside of the logs folder with datetime as name
        creation_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(f"logs/{creation_time}", exist_ok=True)

        # Create file handler
        log_filename = f"logs/{creation_time}/{name}.log"
        file_handler = FileHandler(log_filename)
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Conditionally add console handler
        if print_debug:
            console_handler = StreamHandler()
            console_handler.setLevel(DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

def create_logger(name: str, print_debug: bool) -> Logger:
    logger = Logger(name, print_debug)
    if print_debug:
        logger.debug("Debug mode is enabled.")
    return logger
