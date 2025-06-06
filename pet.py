
from datetime import datetime
from aqt import mw

class AnkiPet:
    def __init__(self):
        self.happiness = 100
        self.hunger = 0
        self.health = 100
        self.level = 1
        self.streak = 0
        self.last_active_day = None

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

    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        self.happiness = min(100, self.happiness + 5)

    def play(self):
        self.happiness = min(100, self.happiness + 10)

    def neglect(self):
        self.hunger = min(100, self.hunger + 10)
        self.happiness = max(0, self.happiness - 15)
        self.health = max(0, self.health - 5)

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
