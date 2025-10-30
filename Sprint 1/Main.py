# Main.py
# Baddie Health Tracker: Sprint 1 - Use Case 1 (Log Daily Mood)
# Runs and displays Expected vs. Actual results for all test cases

from DataStorage import DataStorage
from User import User
from HealthTracker import HealthTracker

def print_test_header(test_id, description):
    print("\n" + "=" * 60)
    print(f"{test_id}: {description}")
    print("=" * 60)

def print_result(expected, actual):
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    print("-" * 60)
    if expected in actual:
        print("Test Result: PASS")
    else:
        print("Test Result: FAIL")
    print("=" * 60 + "\n")

def main():
    # Setup
    db = DataStorage()
    db.add_user("test@example.com", "password123")

    user = User(db)
    user.create_login_ui()
    
    tracker = HealthTracker(db)

    # --- TC01: Successful Login ---
    print_test_header("TC01", "Successful Login")
    expected = "Login successful"
    actual = user.login("test@example.com", "password123")
    print_result(expected, actual)

    # --- TC02: Unsuccessful Login ---
    print_test_header("TC02", "Unsuccessful Login")
    expected = "Error: Invalid email or password"
    actual = user.login("test@example.com", "wrongpass")
    print_result(expected, actual)

    # --- TC03: Successful Mood Streak Update ---
    print_test_header("TC03", "Successful Mood Streak Update")
    user.login("test@example.com", "password123")
    expected = "Mood logged successfully"
    actual = tracker.log_mood("test@example.com", 4)
    print_result(expected, actual)

    # --- TC04: Mood Streak Too Large ---
    print_test_header("TC04", "Mood Streak Too Large")
    db.users["test@example.com"]["streak"] = 9999
    expected = "Error: streak limit reached"
    actual = tracker.log_mood("test@example.com", 4)
    print_result(expected, actual)

if __name__ == "__main__":
    main()
