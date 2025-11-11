# Main_uc3.py
# CLI demo for UC3: shows tip behavior for low moods, opt-out behavior,
# and fallback when the tips service is unavailable.

from datetime import date
from DataStorage_UC3 import DataStorage_UC3
from User_UC3 import User_UC3
from HealthTracker_UC3 import HealthTracker_UC3
from TipsService import TipsService

LINE = "=" * 70

def show(title: str, val) -> None:
    """Pretty-print a section header and message to the console."""
    print(f"\n{LINE}\n{title}\n{LINE}")
    print(val)

if __name__ == "__main__":
    # Setup: user + services
    db = DataStorage_UC3()
    tips = TipsService()
    db.add_user("student@demo.edu", "pw123", tips_opt_out=False)

    user = User_UC3(db)
    assert user.login_cli("student@demo.edu", "pw123") == "Login successful"
    trk = HealthTracker_UC3(db, tips)

    # A) Low mood -> tip shown
    msg = trk.log_mood("student@demo.edu", 1, when=date.today())
    show("UC3.A low mood -> tip shown", msg)

    # B) Opted out -> no tip
    db.set_tips_opt_out("student@demo.edu", True)
    msg = trk.log_mood("student@demo.edu", 2, when=date.today())
    show("UC3.B opted out -> no tip", msg)
    db.set_tips_opt_out("student@demo.edu", False)

    # C) Tips unavailable -> generic supportive message
    tips.available = False
    msg = trk.log_mood("student@demo.edu", 1, when=date.today())
    show("UC3.C outage -> generic supportive message", msg)
