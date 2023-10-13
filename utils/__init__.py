import logging
import os
from datetime import datetime

class modLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super(modLogger,self).__init__(name,level)
    # def emit(self, record):
    #     modify record before printing
    #     print(record.msg)
    def info(self, msg, *args, **kwargs):
        super(modLogger, self).info(msg.strip(), *args, **kwargs)
        print(msg)
    def debug(self, msg, *args, **kwargs):
        super(modLogger, self).debug(msg.strip(), *args, **kwargs)
        print(msg)
    def debug_noprint(self, msg, *args, **kwargs):
        super(modLogger, self).debug(msg.strip(), *args, **kwargs)
        # no print
    def error(self, msg, *args, **kwargs):
        super(modLogger, self).error(msg.strip(), *args, **kwargs)
        print(msg)

os.makedirs('logs', exist_ok=True)

logging.setLoggerClass(modLogger)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler and add it to the logger
file_handler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)6s] - %(message)s'))
logger.addHandler(file_handler)