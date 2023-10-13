import re, time
from . import logger

class custom_input:
    "input gets custom inputs"

    def __init__(self):
        return
    
    def all(self, prompt):
        "accepts everything"
        user_input = input(prompt).strip().lower()
        logger.debug(prompt + "\t|" + user_input + "|")
        return user_input
    
    def acc(self, prompt, accepted_values):
        "accepts scpecific values (case insensitive)"
        user_input = input(prompt).strip().lower()
        if user_input in accepted_values:
            logger.debug(prompt + "\t|" + user_input + "|")
            return user_input
        else:
            return self.acc(prompt, accepted_values)
    
    def int(self, prompt):
        "accepts integers"
        user_input = input(prompt).strip().lower()
        if user_input.isdigit():
            logger.debug(prompt + "\t|" + user_input + "|")
            return int(user_input)
        else:
            return self.int(prompt)
    
    def flo(self, prompt):
        "accepts integers and floats"
        user_input = input(prompt).strip().lower()
        if user_input.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', user_input):
            logger.debug(prompt + "\t|" + user_input + "|")
            return float(user_input)
        else:
            return self.flo(prompt)


class chronometer:
    "chronometer is a chronometer object capable of reset, start, pause, read"

    def __init__(self):
        self.elapsed_time = None
        self.reset()
    
    def reset(self) -> float | None:
        "resets the chronometer and returns elapsed time"
        et = self.elapsed_time
        self.start_time = None
        self.elapsed_time = 0.0
        self.is_running = False
        return et

    def start(self) -> float | None:
        "starts the chronometer and returns start time"

        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            return self.start_time
        else:
            print("Chronometer is already running.")

    def pause(self) -> float | None:
        "stops the chronometer and returns elapsed time"

        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
            return self.elapsed_time
        else:
            print("Chronometer is not running.")

    def read(self) -> float | None: # self.elapsed_time might be None
        "returns elapsed time"
        if self.is_running:
            return self.elapsed_time + (time.time() - self.start_time)
        else:
            return self.elapsed_time

