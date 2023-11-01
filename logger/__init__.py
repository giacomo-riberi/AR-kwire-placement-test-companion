import os
import logging
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
    def debug_input(self, msg, *args, **kwargs):
        "debug_input but does not print to terminal, logs on file only"
        super(modLogger, self).debug(msg.strip(), *args, **kwargs)
        # no print
    def error(self, msg, *args, **kwargs):
        super(modLogger, self).error(msg.strip(), *args, **kwargs)
        print(msg)
    def critical(self, msg, *args, **kwargs):
        "critical will log critical level and quit"
        super(modLogger, self).critical(msg.strip(), *args, **kwargs)
        print(msg)
        quit()


os.makedirs('logs', exist_ok=True)
logging.setLoggerClass(modLogger)
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)6s] - %(message)s'))
logger.addHandler(file_handler)