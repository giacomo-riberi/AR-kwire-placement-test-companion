import data
import time
import re
import json

from logger import logger # local

version = "v1.27"
db_name = f"./db/positioning_test_data-({version}).db"

class custom_input:
    "input gets custom inputs"

    def __init__(self):
        return
    
    def acc(self, prompt: str, accepted_values) -> str:
        "accepts specific values (case insensitive)"
        user_input = input(f"{prompt} {accepted_values}: ").strip().lower()
        if user_input in accepted_values:
            logger.debug_input(prompt + "\t|" + user_input + "|")
            return user_input
        else:
            return self.acc(prompt, accepted_values)

    def boo(self, prompt: str) -> bool:
        "accepts yes/no values (case insensitive)"
        user_input = input(prompt).strip().lower()
        if user_input in ["y", "yes", "1", "true"]:
            logger.debug_input(prompt + "\t|" + user_input + "|")
            return True
        elif user_input in ["n", "no", "0", "false"]:
            logger.debug_input(prompt + "\t|" + user_input + "|")
            return False
        else:
            return self.boo(prompt)
    
    def int(self, prompt: str, min=-1000000, max=1000000) -> int:
        "accepts integers in specified range"
        user_input = input(prompt).strip().lower()

        try:
            user_int = int(user_input)
            if min <= user_int <= max:
                logger.debug_input(prompt + "\t|" + user_input + "|")
                return user_int
            else:
                raise
        except Exception:
            return self.int(prompt, min, max)
    
    def flo(self, prompt: str, default: float=None, min: float=-1000000.0, max: float=1000000) -> float:
        "accepts integers and floats"        
        user_input = input(prompt).strip().lower()

        if user_input == "":
            user_input = default

        try:
            user_float = float(user_input)
            if min <= user_float <= max:
                logger.debug_input(prompt + f"{prompt}\t|{user_input}|")
                return user_float
            else:
                raise
        except Exception as e:
            return self.flo(prompt, default, min, max)
        
    def str(self, prompt: str, minlen=0, maxlen=1000000) -> str:
        "accepts strings, min and max lenght can be specified"
        user_input = input(prompt).strip().lower()
        if minlen <= len(user_input) <= maxlen:
            logger.debug_input(prompt + "\t|" + user_input + "|")
            return user_input            
        else:
            return self.str(prompt, minlen, maxlen)
    
    def PAdata_computed(self, prompt, id_orig) -> data.PAdata:
        "accepts json string of PA data after fusion 360 computation"
        user_input = input(prompt)
        try:
            PA_data = data.PAdata(**json.loads(user_input))
            if not PA_data.fusion_computed:
                raise Exception("data has not been computed by fusion!")
            if PA_data.id != id_orig:
                raise Exception("a wild id came back!")
            logger.debug_input(prompt + "\t|" + user_input + "|")
            return PA_data
        except Exception as e:
            print(f"ERROR: {e}\n")
            return self.PAdata_computed(prompt, id_orig)

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
        if et == None:
            return et
        else:
            return round(et, 2)

    def start(self) -> float | None:
        "starts the chronometer and returns start time"

        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            return round(self.start_time, 2)
        else:
            print("Chronometer is already running.")

    def pause(self) -> float | None:
        "stops the chronometer and returns elapsed time"

        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
            return round(self.start_time, 2)
        else:
            print("Chronometer is not running.")

    def read(self) -> float | None: # self.elapsed_time might be None
        "returns elapsed time"
        if self.is_running:
            return round(self.elapsed_time + (time.time() - self.start_time), 2)
        else:
            return round(self.start_time, 2)
