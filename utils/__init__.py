import logging
import os
from datetime import datetime

class screenPrint(logging.Handler):
    def emit(self, record):
        if record.levelno == logging.DEBUG: # debug is used for custom_input (trick used to not have a double message on screen)
            return
        print(record.msg)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and add it to the logger
os.makedirs('logs', exist_ok=True)
file_handler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - [%(levelname)8s] - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)
logger.addHandler(screenPrint())