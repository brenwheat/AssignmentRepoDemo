# Tests.py
# Automated test cases for Activity 3 Sprint 1

from DataStorage import DataStorage
from User import User
from HealthTracker import HealthTracker

def run_tests():
    db = DataStorage()
    db.add_user("test@example.com", "password123")
    user = User(db)
    tracker = HealthTracker(db)

    print("Running Test Cases...\n")

    # TC01
    result1 = user.login("test@example.com", "password123")
    print("TC01 - Successful Login:", "PASS" if "successful" in result1 else "FAIL")

    # TC02
    result2 = user.login("test@example.com", "wrongpass")
    print("TC02 - Unsuccessful Login:", "PASS" if "Invalid" in result2 else "FAIL")

    # TC03
    user.login("test@example.com", "password123")
    result3 = tracker.log_mood("test@example.com", 4)
    print("TC03 - Successful Mood Streak Update:", "PASS" if "Mood logged" in result3 else "FAIL")

    # TC04
    db.users["test@example.com"]["streak"] = 9999
    result4 = tracker.log_mood("test@example.com", 4)
    print("TC04 - Mood Streak Too Large:", "PASS" if "limit" in result4 else "FAIL")

if __name__ == "__main__":
    run_tests()
