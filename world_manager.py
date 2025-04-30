import random
import datetime
import os
import json
from choice_engine import ChoiceEngine
from world_templates import generate_ai_world_template  # v1.0+ GPT-powered world generation

PLAYER_FOLDER = "data/players"

class WorldManager:
    def __init__(self):
        pass  # Worlds are dynamically generated!

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

            # ✨ Track past visited worlds
            data.setdefault("PastWorlds", [])
            if world_name not in data["PastWorlds"]:
                data["PastWorlds"].append(world_name)

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️ Failed to update player file: {e}")

    def generate_scene_choices(self):
        engine = ChoiceEngine()
        engine.generate_choices()
        return (
            engine.choices,
            engine.death_choice,
            engine.progress_choice,
            engine.lore_choices,
            engine.random_choice
        )
