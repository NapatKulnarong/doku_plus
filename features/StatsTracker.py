import csv
from datetime import datetime
import os
from typing import Optional


class StatsTracker:
    def __init__(self, filename: str = "game_stats.csv"):
        """
        Initialize the stats tracker with a CSV file.

        Args:
            filename: Name of the CSV file to store stats (default: game_stats.csv)
        """
        # Get the project root directory (2 levels up from this file)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Define paths
        self.data_dir = os.path.join(self.project_root, 'data')
        self.filepath = os.path.join(self.data_dir, filename)

        # Ensure directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize CSV file with headers if needed
        self._initialize_file()

    def _initialize_file(self) -> None:
        """Create the stats file with headers if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self._get_fieldnames())
                writer.writeheader()

    @staticmethod
    def _get_fieldnames() -> list:
        """Return the field names for the CSV file."""
        return [
            "Timestamp",  # Date & time of the game session (YYYY-MM-DD HH:MM:SS)
            "Difficulty",  # Game difficulty (easy, medium, hard, advanced)
            "Time",  # Time taken in MM:SS format
            "Mistakes",  # Total number of mistakes made (integer)
            "Hints Used",  # Number of hints used (integer)
            "Win",  # Result ("Win" or "Loss")
            "Filled Cells"  # Number of manually filled cells (integer)
        ]

    def log_game(
            self,
            difficulty: str,
            time_taken: str,
            mistakes: int,
            hints_used: int,
            win: bool,
            filled_cells: int
    ) -> None:
        """
        Log a game session to the stats file.

        Args:
            difficulty: Game difficulty level
            time_taken: Time taken in MM:SS format
            mistakes: Number of mistakes made
            hints_used: Number of hints used
            win: Whether the game was won
            filled_cells: Number of cells filled by the player
        """
        with open(self.filepath, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self._get_fieldnames())
            writer.writerow({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Difficulty": difficulty.lower(),
                "Time": time_taken,
                "Mistakes": mistakes,
                "Hints Used": hints_used,
                "Win": "Win" if win else "Loss",
                "Filled Cells": filled_cells
            })

    def get_recent_games(self, count: int = 5) -> Optional[list[dict]]:
        """
        Get recent game sessions from the stats file.

        Args:
            count: Number of recent games to retrieve

        Returns:
            List of dictionaries containing game data, or None if file doesn't exist
        """
        if not os.path.exists(self.filepath):
            return None

        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            games = list(reader)

        return games[-count:][::-1]  # Return most recent first

    def clear_stats(self) -> None:
        """Clear all statistics by recreating the file with just headers."""
        self._initialize_file()