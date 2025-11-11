# Tests_uc3.py
# Simple assertions that cover UC3 behaviors:
#  - Tip shown when mood is 1 (unless outage)
#  - Tips suppressed when opted out
#  - Generic fallback when service unavailable
#  - No tip for normal moods (>=3)

from datetime import date
from DataStorage_UC3 import DataStorage_UC3
from User_UC3 import User_UC3
from HealthTracker_UC3 import HealthTracker_UC3
from TipsService import TipsService

def run_tests():
    db = DataStorage_UC3()
    tips = TipsService()
    db.add_user("u@x.com", "p", tips_opt_out=False)

    user = User_UC3(db)
    assert user.login_cli("u@x.com", "p") == "Login successful"

    trk = HealthTracker_UC3(db, tips)

    # 1) Low mood -> tip
    m1 = trk.log_mood("u@x.com", 1, when=date.today())
    assert ("Tip:" in m1) or ("Remember, you’re not alone." in m1)

    # 2) Opt-out -> no tip
    db.set_tips_opt_out("u@x.com", True)
    m2 = trk.log_mood("u@x.com", 2, when=date.today())
    assert "Tips are turned off." in m2

    # 3) Outage -> generic fallback
    db.set_tips_opt_out("u@x.com", False)
    tips.available = False
    m3 = trk.log_mood("u@x.com", 1, when=date.today())
    assert "Remember, you’re not alone." in m3

    # 4) Normal mood -> no tip text
    tips.available = True
    m4 = trk.log_mood("u@x.com", 3, when=date.today())
    assert "Tip:" not in m4

    print("UC3 tests passed.")

if __name__ == "__main__":
    run_tests()
