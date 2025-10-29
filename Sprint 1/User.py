# User.py
# Handles login functionality

from DataStorage import DataStorage

class User:
    def __init__(self, storage):
        self.storage = storage
        self.logged_in_user = None

    def login(self, email, password):
        if self.storage.validate_login(email, password):
            self.logged_in_user = email
            return "Login successful"
        else:
            return "Error: Invalid email or password"
