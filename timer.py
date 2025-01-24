import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time:
            self.end_time = time.time()
            elapsed_time = self.end_time - self.start_time
            self.start_time = None  # Reset timer
            return int(elapsed_time)
        return 0