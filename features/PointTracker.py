import os
import json

class PointTracker:
    def __init__(self, user_manager, username):
        self.user_manager = user_manager  # Store reference to user manager
        self.username = username

        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        self.filename = os.path.join(self.data_dir, f"points_{self.username}.json")
        self.points = 0
        self.level = 1

        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.points = data.get("points", 0)
                self.level = data.get("level", self.calculate_level())
        else:
            # Fallback to data from user manager if available
            user_data = self.user_manager.get_user_data(self.username)
            self.points = user_data.get("points", 0)
            self.level = user_data.get("level", self.calculate_level())
            self.save_data()

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump({"points": self.points, "level": self.level}, file)

        # Also update user manager if supported
        if hasattr(self.user_manager, 'update_user_points'):
            self.user_manager.update_user_points(self.username, self.points, self.level)

    def calculate_level(self):
        return (self.points // 100) + 1

    def add_points(self, points):
        self.points += points
        leveled_up = False
        while self.points >= 100:
            self.points -= 100
            self.level += 1
            leveled_up = True

        self.save_data()

        # ✅ Sync back to users.json
        if self.user_manager:
            self.user_manager.update_user_stats(self.username, self.points, self.level)

        return leveled_up

    def update_points(self, new_total):
        self.points = max(0, new_total)
        self.level = self.calculate_level()
        self.save_data()

    def get_points(self):
        return self.points

    def get_level(self):
        return self.level

    def get_data(self):
        return {
            "points": self.points,
            "level": self.level
        }