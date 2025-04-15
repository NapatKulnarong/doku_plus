import json
import os


class UserManager:
    def __init__(self, data_dir="data", filename="users.json"):
        # Set the directory and filename for storing user data
        self.data_dir = data_dir
        self.filename = os.path.join(self.data_dir, filename)

        # Make sure the directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize user data: either load from file or start fresh
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            self.users = {}              # Start with an empty dictionary if no file or empty file
            self.save_users()           # Save the initial empty structure
        else:
            self.users = self.load_users()  # Load existing users from file

    def load_users(self):
        # Load user data from the JSON file
        with open(self.filename, "r") as file:
            return json.load(file)

    def save_users(self):
        # Save the current user data to the JSON file
        with open(self.filename, "w") as file:
            json.dump(self.users, file, indent=4)  # Save with formatting for readability

    def add_user(self, username, password_hash, avatar):
        # Add a new user with hashed password and avatar, no points/level yet
        self.users[username] = {
            "password_hash": password_hash,
            "avatar": avatar
        }
        self.save_users()  # Save changes to file

    def user_exists(self, username):
        # Check if the given username is already registered
        return username in self.users

    def verify_password(self, username, password_hash):
        # Check if the password hash matches the stored one
        return self.users[username]["password_hash"] == password_hash

    def get_avatar(self, username):
        # Get the avatar associated with the user
        return self.users[username].get("avatar", None)

    def update_user_stats(self, username, points, level):
        # Update the user's points and level (used for syncing with game progress)
        if username in self.users:
            self.users[username]['points'] = points
            self.users[username]['level'] = level
            self.save_users()  # Save changes to file
