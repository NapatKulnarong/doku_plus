import json
import os


class UserManager:
    def __init__(self, data_dir="data", filename="users.json"):
        self.data_dir = data_dir
        self.filename = os.path.join(self.data_dir, filename)

        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            self.users = {}
            self.save_users()
        else:
            self.users = self.load_users()

    def load_users(self):
        with open(self.filename, "r") as file:
            return json.load(file)

    def save_users(self):
        with open(self.filename, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, username, password_hash, avatar):
        self.users[username] = {
            "password_hash": password_hash,
            "avatar": avatar
        }
        self.save_users()

    def user_exists(self, username):
        return username in self.users

    def verify_password(self, username, password_hash):
        return self.users[username]["password_hash"] == password_hash

    def get_avatar(self, username):
        return self.users[username].get("avatar", None)

    def get_user_data(self, username):
        return self.users.get(username, {})

    def update_user_stats(self, username, points, level):
        if username in self.users:
            self.users[username]['points'] = points
            self.users[username]['level'] = level
            self.save_users()

    def get_top_users(self, limit=None):
        sorted_users = sorted(
            self.users.items(),
            key=lambda item: (item[1].get("level", 1), item[1].get("points", 0)),
            reverse=True
        )
        if limit:
            return sorted_users[:limit]
        return sorted_users