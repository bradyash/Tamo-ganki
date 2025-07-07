
from datetime import datetime
from aqt import mw

class AnkiPet:
    def __init__(self):
        # Load persisted stats if available
        saved = mw.pm.profile.get("ankipet_stats", {})
        self.happiness = saved.get("happiness", 100)
        self.hunger = saved.get("hunger", 0)
        self.health = saved.get("health", 100)
        self.level = saved.get("level", 1)
        self.streak = saved.get("streak", 0)
        # Last active day is loaded separately
        self.last_active_day = self.load_last_active_day()

    def load_last_active_day(self):
        saved = mw.pm.profile.get("ankipet_last_active")
        if saved:
            try:
                return datetime.strptime(saved, "%Y-%m-%d").date()
            except Exception:
                return None
        return None

    def save_last_active_day(self, day):
        mw.pm.profile["ankipet_last_active"] = day.strftime("%Y-%m-%d")
        mw.pm.save()

    def save_stats(self):
        mw.pm.profile["ankipet_stats"] = {
            "happiness": self.happiness,
            "hunger": self.hunger,
            "health": self.health,
            "level": self.level,
            "streak": self.streak,
        }
        mw.pm.save()

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.happiness = min(100, self.happiness + 5)
        self.save_stats()

    def play(self):
        self.happiness = min(100, self.happiness + 10)
        self.save_stats()

    def neglect(self):
        self.hunger = min(100, self.hunger + 10)
        self.happiness = max(0, self.happiness - 15)
        self.health = max(0, self.health - 5)
        self.save_stats()

    def check_streak(self, today):
        if self.last_active_day is None:
            self.streak = 1
        else:
            days_missed = (today - self.last_active_day).days
            if days_missed == 1:
                self.streak += 1
            elif days_missed > 1:
                self.streak = 1
                missed = days_missed - 1
                self.health = max(0, self.health - (missed * 10))
                self.happiness = max(0, self.happiness - (missed * 5))
                self.hunger = min(100, self.hunger + (missed * 10))
        self.last_active_day = today
        self.save_last_active_day(today)
        self.save_stats()
