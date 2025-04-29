import random
from procedural_companion_generator import ProceduralCompanionGenerator

class CompanionManager:
    def __init__(self):
        pass  # No need to pre-load fixed companions anymore!

    def random_companion_encounter(self):
        """Randomly decide if a companion appears. 20% chance."""
        chance = random.randint(1, 100)
        if chance <= 20:
            return ProceduralCompanionGenerator.generate_companion()
        else:
            return None
