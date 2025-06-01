import json
import os

class TimelineShard:
    def __init__(self, world_name, year):
        self.world = world_name
        self.year = year
        self.events = []

    def log_event(self, character, description, year=None, phase=None):
        entry = {
            "character": character,
            "description": description,
            "year": year or self.year,
            "phase": phase or "Unknown"
        }
        self.events.append(entry)

    def get_events(self):
        return self.events

    def shard_summary(self):
        return f"{self.world} – Year {self.year}: {len(self.events)} events logged."

    def save(self, path="data/shards/"):
        os.makedirs(path, exist_ok=True)
        filename = f"{self.world.replace(' ', '_')}_{self.year}.json"
        with open(os.path.join(path, filename), "w") as f:
            json.dump({"world": self.world, "year": self.year, "events": self.events}, f, indent=2)

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        shard = TimelineShard(data["world"], data["year"])
        shard.events = data["events"]
        return shard