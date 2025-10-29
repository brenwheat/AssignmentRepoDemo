# Main.py
# Runs the app and simulates test case execution

from DataStorage import DataStorage
from User import User
from HealthTracker import HealthTracker

def main():
    db = DataStorage()
    db.add_user("test@example.com", "password123")

    user = User(db)
    tracker = HealthTracker(db)

    print("=== TC01: Successful Login ===")
    print(user.login("test@example.com", "password123"))  # Expected: successful login

    print("\n=== TC02: Unsuccessful Login ===")
    print(user.login("test@example.com", "wrongpass"))  # Expected: error message

    print("\n=== TC03: Successful Mood Streak Update ===")
    user.login("test@example.com", "password123")
    print(tracker.log_mood("test@example.com", 4))  # Expected: success message with streak count

    print("\n=== TC04: Mood Streak Number Too Large ===")
    db.users["test@example.com"]["streak"] = 9999
    print(tracker.log_mood("test@example.com", 4))  # Expected: streak limit error

if __name__ == "__main__":
    main()
