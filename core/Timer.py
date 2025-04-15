import time


class Timer:
    def __init__(self):
        # Initialize timer: record the start time, set elapsed to 0, and mark it as running
        self.start_time = time.time()
        self.elapsed_time = 0
        self.running = True

    def update(self):
        # Continuously update elapsed_time only when the timer is running
        if self.running:
            self.elapsed_time = time.time() - self.start_time

    def pause(self):
        # Pause the timer and store the current elapsed time
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False  # Mark as paused

    def resume(self):
        # Resume the timer by recalculating the start_time offset
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def reset(self):
        # Reset the timer to start counting fresh from now
        self.start_time = time.time()
        self.elapsed_time = 0
        self.running = True

    def get_time_string(self):
        # Return the elapsed time as a formatted string MM:SS
        minutes, seconds = divmod(int(self.elapsed_time), 60)
        return f"{minutes:02d}:{seconds:02d}"
