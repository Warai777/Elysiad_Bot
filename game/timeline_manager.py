from datetime import datetime

class TimelineShard:
    def __init__(self, world_name, base_year):
        self.world_name = world_name
        self.base_year = base_year
        self.events = []  # {"player": ..., "event": ..., "year": ..., "phase": ...}

    def log_event(self, player_name, event_desc, year, phase):
        self.events.append({
            "player": player_name,
            "event": event_desc,
            "year": year,
            "phase": phase,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_events_by_year(self, year):
        return [e for e in self.events if e["year"] == year]

    def get_events_in_range(self, start_year, end_year):
        return [e for e in self.events if start_year <= e["year"] <= end_year]

    def shard_summary(self):
        return f"{self.world_name} Shard: {len(self.events)} events from {self.base_year}"