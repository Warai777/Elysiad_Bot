import os
import json
import random

PLAYER_FOLDER = "data/players"

if not os.path.exists(PLAYER_FOLDER):
    os.makedirs(PLAYER_FOLDER)

class Player:
    def __init__(self, name, background, genre):
        self.name = name
        self.background = background
        self.genre = genre
        self.traits = self.assign_random_traits()
        self.alignment = {
            "Bravery": 0,
            "Cruelty": 0,
            "Wisdom": 0,
            "Compassion": 0,
            "Foolishness": 0
        }
        self.will = {
            "WillToLive": 0,
            "WillToSacrifice": 0
        }
        self.current_world = None
        self.world_entry_time = None

    def assign_random_traits(self):
        traits = ["Curious", "Bold", "Quiet", "Impulsive", "Cautious", "Charming"]
        return random.sample(traits, 2)

    def save(self):
        filepath = os.path.join(PLAYER_FOLDER, f"{self.name}.json")
        with open(filepath, "w") as f:
            json.dump(self.__dict__, f, indent=2)

    @classmethod
    def load(cls, name):
        filepath = os.path.join(PLAYER_FOLDER, f"{name}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            data = json.load(f)
        player = cls(data["name"], data["background"], data["genre"])
        player.traits = data["traits"]
        player.alignment = data["alignment"]
        player.will = data["will"]
        player.current_world = data.get("current_world")
        player.world_entry_time = data.get("world_entry_time")
        return player

    def save_now(self):
        self.save()
