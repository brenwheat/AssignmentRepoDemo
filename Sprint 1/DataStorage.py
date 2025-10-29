# DataStorage.py
# Simulates an in-memory database for users and mood logs

class DataStorage:
    def __init__(self):
        # Example user format: {"password": "abc123", "streak": 0, "moods": []}
        self.users = {}

    def add_user(self, email, password):
        self.users[email] = {"password": password, "streak": 0, "moods": []}

    def validate_login(self, email, password):
        user = self.users.get(email)
        if user and user["password"] == password:
            return True
        return False

    def save_mood(self, email, mood):
        """Save a mood value for a user"""
        if email not in self.users:
            return "Error: User not found"
        self.users[email]["moods"].append(mood)
        return "Mood saved"

    def get_streak(self, email):
        return self.users[email]["streak"]

    def update_streak(self, email):
        """Increase streak unless limit (9999) reached"""
        user = self.users[email]
        if user["streak"] >= 9999:
            return "Error: streak limit reached"
        user["streak"] += 1
        return user["streak"]
