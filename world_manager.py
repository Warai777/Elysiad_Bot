import random
import datetime
import os
import json
from choice_engine import ChoiceEngine   # <-- Import ChoiceEngine properly here
from world_templates import generate_world

PLAYER_FOLDER = "data/players"

class WorldManager:
    def __init__(self):
        self.world_names_pool = [
            "Sea of Endless Horizons",
            "Realm of Silent Shadows",
            "City of Hollow Dreams",
            "Forest of Distant Echoes",
            "Vault of Shattered Stars",
            "Labyrinth of Forgotten Sins",
            "The Bleeding Mirror",
            "Twilight Cradle",
            "The Wounded Sky",
            "Crown of Falling Leaves"
        ]

    def generate_books(self):
    return [generate_world() for _ in range(3)]

    def start_world_timer(self, player_name, world_name):
        filepath = os.path.join(PLAYER_FOLDER, f"{player_name}.json")
        if not os.path.exists(filepath):
            return

        with open(filepath, "r") as f:
            data = json.load(f)

        data["current_world"] = world_name
        data["world_entry_time"] = datetime.datetime.utcnow().isoformat()

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def generate_scene_choices(self):
        engine = ChoiceEngine()
        engine.generate_choices()
        return engine.choices, engine.death_choice, engine.progress_choice, engine.lore_choices, engine.random_choice
