import re, time

def custom_input(prompt, accepted_values):
    "custom_input behaves like input but continues to prompt the user until the input matches one of the accepted values"

    while True:
        user_input = input(prompt).strip().lower()  
        if user_input == "":
            continue
        if user_input in accepted_values:
            return user_input
        elif accepted_values == "INTEGER" and user_input.isdigit():
            return int(user_input)
        elif accepted_values == "FLOAT" and (user_input.isdigit() or re.match(r'^-?\d+(?:\.\d+)$', user_input) != None):
            return float(user_input)

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