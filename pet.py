
from datetime import datetime, timedelta
from aqt import mw

class AnkiPet:
    def __init__(self):
        # Load persisted stats if available. ``mw.pm.profile`` is not available
        # until a profile has been opened, so guard against ``None`` to avoid
        # crashes when the add-on is imported before that happens.
        profile = getattr(mw.pm, "profile", None) if getattr(mw, "pm", None) else None
        saved = profile.get("ankipet_stats", {}) if profile else {}
        self.happiness = saved.get("happiness", 100)
        self.hunger = saved.get("hunger", 0)
        self.health = saved.get("health", 100)
        self.level = saved.get("level", 1)
        self.streak = saved.get("streak", 0)
        # Last active day is loaded separately
        self.last_active_day = self.load_last_active_day()

    def load_last_active_day(self):
        profile = getattr(mw.pm, "profile", None) if getattr(mw, "pm", None) else None
        saved = profile.get("ankipet_last_active") if profile else None
        if saved:
            try:
                return datetime.strptime(saved, "%Y-%m-%d").date()
            except Exception:
                return None
        return None

    def save_last_active_day(self, day):
        profile = getattr(mw.pm, "profile", None) if getattr(mw, "pm", None) else None
        if profile:
            profile["ankipet_last_active"] = day.strftime("%Y-%m-%d")
            mw.pm.save()

    def save_stats(self):
        profile = getattr(mw.pm, "profile", None) if getattr(mw, "pm", None) else None
        if profile:
            profile["ankipet_stats"] = {
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
        # Determine the current streak based on Anki's revlog rather than
        # the plugin's stored state. Anki stores all review activity in the
        # ``revlog`` table, and ``day_cutoff`` marks the start of the next day
        # according to the collection's settings. By grouping the revlog entries
        # by their distance from ``day_cutoff`` we can count how many consecutive
        # days have had study activity, starting from today.

        day_cutoff = mw.col.sched.day_cutoff
        days = mw.col.db.list(
            """
select cast((? - id/1000) / 86400 as int) as day
from revlog
group by day
""",
            day_cutoff,
        )
        day_set = set(days)
        streak = 0
        while streak in day_set:
            streak += 1
        self.streak = streak

        # Apply penalties for full days without any study activity. We only
        # penalize days that have fully elapsed (yesterday and earlier) and
        # avoid double‑counting by tracking the last day already handled.
        yesterday = today - timedelta(days=1)
        if self.last_active_day is None:
            self.last_active_day = yesterday if 0 not in day_set else today
        else:
            if yesterday > self.last_active_day:
                missed = (yesterday - self.last_active_day).days
                self.health = max(0, self.health - (missed * 10))
                self.happiness = max(0, self.happiness - (missed * 5))
                self.hunger = min(100, self.hunger + (missed * 10))
                self.last_active_day = self.last_active_day + timedelta(days=missed)
            if 0 in day_set:
                self.last_active_day = today

        self.save_last_active_day(self.last_active_day)
        self.save_stats()
