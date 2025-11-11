# User.py
# Minimal authentication wrapper suitable for CLI-based tests.

class User:
    def __init__(self, storage) -> None:
        # storage must provide validate_login(email, password)
        self.storage = storage
        self.logged_in_user = None

    def login_cli(self, email: str, password: str) -> str:
        """
        Attempt to log in. On success, set logged_in_user for later actions.
        Returns a human-readable message for the CLI demo.
        """
        if self.storage.validate_login(email, password):
            self.logged_in_user = email
            return "Login successful"
        return "Error: Invalid email or password"
