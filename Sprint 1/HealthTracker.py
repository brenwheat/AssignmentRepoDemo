# HealthTracker.py
# Handles logging moods and updating streaks

class HealthTracker:
    def __init__(self, storage):
        self.storage = storage

    def log_mood(self, email, mood):
        if mood < 1 or mood > 5:
            return "Invalid mood value. Must be between 1 and 5."

        save_status = self.storage.save_mood(email, mood)
        if "Error" in save_status:
            return save_status

        streak_update = self.storage.update_streak(email)
        if isinstance(streak_update, str) and "Error" in streak_update:
            return streak_update

        return f"Mood logged successfully, you are on a {streak_update}-day streak"
