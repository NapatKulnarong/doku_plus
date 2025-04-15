import csv
from datetime import datetime
import os

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StatsTracker:
    def __init__(self, filename="game_stats.csv"):
        # Define the directory to save the stats file (in /data)
        self.data_dir = os.path.join(PROJECT_ROOT, 'data')

        # Full path to the CSV file
        self.filename = os.path.join(self.data_dir, filename)

        # Make sure the data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        print(f"Saving stats to: {self.filename}")

        # Create the file with headers if it doesn't exist
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """
        Create the stats file and write headers if it doesn't already exist.
        """
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow([
                    "Timestamp",      # Date & time of the game session
                    "Difficulty",     # Game difficulty (easy, medium, etc.)
                    "Time",           # Time taken in mm:ss format
                    "Mistakes",       # Total number of mistakes made
                    "Hints Used",     # Number of hints used
                    "Win",            # Result (Win or Loss)
                    "Filled Cells"    # Number of manually filled cells
                ])

    def log_game(self, difficulty, time_taken, mistakes, hints_used, win, filled_cells):
        """
        Append a row of game result data to the stats CSV file.
        """
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
                difficulty,      # Difficulty level of the game
                time_taken,      # Time it took to complete the game
                mistakes,        # Number of mistakes made
                hints_used,      # Number of hints used
                "Win" if win else "Loss",  # Convert win boolean to readable text
                filled_cells     # Manually filled cells (not hint-based)
            ])
            file.flush()  # Ensure data is written immediately to disk
