import json
import os
import random

COMPANION_FILE = "data/companions.json"

class CompanionManager:
    def __init__(self):
        if os.path.exists(COMPANION_FILE):
            with open(COMPANION_FILE, "r") as f:
                self.all_companions = json.load(f)
        else:
            self.all_companions = []

    def random_companion_encounter(self):
        """Randomly decide if a companion appears. 20% chance."""
        chance = random.randint(1, 100)
        if chance <= 20 and self.all_companions:
            return random.choice(self.all_companions)
        else:
            return None
