import os
import json

class Player:
    def __init__(self, name, background, trait):
        self.name = name
        self.background = background
        self.trait = trait
        self.memory = {
            "Journal": {
                "Hints": [],
                "Lore": [],
                "Events": [],
                "Notes": []
            }
        }

    def save(self):
        with open(f"data/players/{self.name}.json", "w") as f:
            json.dump(self.__dict__, f, indent=2)

    @classmethod
    def load(cls, name):
        try:
            with open(f"data/players/{name}.json") as f:
                data = json.load(f)
                p = cls(data['name'], data['background'], data['trait'])
                p.memory = data.get('memory', p.memory)
                return p
        except FileNotFoundError:
            return cls(name, "Unknown", "Unknown")

def load_player(name):
    return Player.load(name)