import csv
from datetime import datetime
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class StatsTracker:
    def __init__(self, filename="game_stats.csv"):
        # Ensure it saves to the /data folder
        self.data_dir = os.path.join(PROJECT_ROOT, 'data')
        self.filename = os.path.join(self.data_dir, filename)

        # Ensure the directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        print(f"Saving stats to: {self.filename}")

        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Difficulty", "Time", "Mistakes", "Hints Used", "Win", "Filled Cells"])

    def log_game(self, difficulty, time_taken, mistakes, hints_used, win, filled_cells):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                difficulty,
                time_taken,
                mistakes,
                hints_used,
                "Win" if win else "Loss",
                filled_cells
            ])
            file.flush()
