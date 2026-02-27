import json
import os


class DataManager:
    """Handles all file persistence logic for the ATM system."""

    def __init__(self, folder="data"):
        self.folder = folder
        self.users_file = os.path.join(self.folder, "users.json")
        self.admins_file = os.path.join(self.folder, "admins.json")

        # Ensure the data directory exists
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def save_data(self, data, filename):
        """Generic write function """
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self, filename):
        """Generic read function """
        if not os.path.exists(filename):
            return {}
        with open(filename, 'r') as f:
            return json.load(f)