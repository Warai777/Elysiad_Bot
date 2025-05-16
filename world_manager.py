import random
import datetime
import os
import json
from world_templates import generate_ai_world_template

PLAYER_FOLDER = "data/players"

class WorldState:
    def __init__(self, name, era="", region="", phase="", shard_id=""):
        self.name = name
        self.era = era
        self.region = region
        self.phase = phase
        self.shard_id = shard_id

    def to_dict(self):
        return {
            "name": self.name,
            "era": self.era,
            "region": self.region,
            "phase": self.phase,
            "shard_id": self.shard_id
        }

    @staticmethod
    def from_dict(data):
        return WorldState(
            name=data.get("name", "Unknown"),
            era=data.get("era", ""),
            region=data.get("region", ""),
            phase=data.get("phase", ""),
            shard_id=data.get("shard_id", "")
        )

class WorldManager:
    def __init__(self):
        pass

    def generate_books(self):
        books = []
        for _ in range(3):
            try:
                book = generate_ai_world_template()
                books.append(book)
            except Exception as e:
                print(f"⚠️ Failed to generate book: {e}")
        return books

    def start_world_timer(self, player_name, world_name):
        filepath = os.path.join(PLAYER_FOLDER, f"{player_name}.json")
        if not os.path.exists(filepath):
            print(f"⚠️ Player file not found: {filepath}")
            return

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            data["current_world"] = world_name
            data["world_entry_time"] = datetime.datetime.utcnow().isoformat()
            data.setdefault("PastWorlds", [])
            if world_name not in data["PastWorlds"]:
                data["PastWorlds"].append(world_name)

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️ Failed to update player file: {e}")