# User_UC3.py
# Minimal authentication wrapper for UC3 demos/tests.

class User_UC3:
    def __init__(self, storage) -> None:
        self.storage = storage
        self.logged_in_user = None

    def login_cli(self, email: str, password: str) -> str:
        """Attempt login; set logged_in_user on success."""
        if self.storage.validate_login(email, password):
            self.logged_in_user = email
            return "Login successful"
        return "Error: Invalid email or password"
