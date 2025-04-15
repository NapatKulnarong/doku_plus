import os
import json


class PointTracker:
    def __init__(self, user_manager, username):
        self.user_manager = user_manager  # Reference to UserManager for syncing data
        self.username = username          # Username this tracker is associated with

        # Define directory for storing per-user point data
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)  # Create data directory if it doesn't exist

        # File path for storing this user's points
        self.filename = os.path.join(self.data_dir, f"points_{self.username}.json")

        self.points = 0  # Points currently earned toward level
        self.level = 1   # Current level based on points

        # Load existing data (from points file or user manager)
        self.load_data()

    def load_data(self):
        # Load data from individual user JSON file
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.points = data.get("points", 0)
                self.level = data.get("level", self.calculate_level())
        else:
            # If file doesn't exist, fallback to data from users.json (UserManager)
            user_data = self.user_manager.get_user_data(self.username)
            self.points = user_data.get("points", 0)
            self.level = user_data.get("level", self.calculate_level())
            self.save_data()  # Save this data into the dedicated file

    def save_data(self):
        # Save point and level data into user's points JSON file
        with open(self.filename, 'w') as file:
            json.dump({"points": self.points, "level": self.level}, file)

        # Optionally update the main users.json if supported
        if hasattr(self.user_manager, 'update_user_points'):
            self.user_manager.update_user_points(self.username, self.points, self.level)

    def calculate_level(self):
        # Level is determined by how many full 100-point segments have been reached
        return (self.points // 100) + 1

    def add_points(self, points):
        # Add points and check if user levels up
        self.points += points
        leveled_up = False

        # Handle level-up logic (reduce 100 points for each level-up)
        while self.points >= 100:
            self.points -= 100
            self.level += 1
            leveled_up = True

        self.save_data()  # Persist changes

        # Also sync back to users.json via UserManager
        if self.user_manager:
            self.user_manager.update_user_stats(self.username, self.points, self.level)

        return leveled_up

    def update_points(self, new_total):
        # Replace current points with a new value (usually reset or correction)
        self.points = max(0, new_total)
        self.level = self.calculate_level()
        self.save_data()  # Persist changes

    def get_points(self):
        # Return current point value
        return self.points

    def get_level(self):
        # Return current level
        return self.level

    def get_data(self):
        # Return both point and level data in dictionary form
        return {
            "points": self.points,
            "level": self.level
        }
