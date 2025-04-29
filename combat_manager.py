import random
from combat_story_manager import CombatStoryManager

class CombatManager:
    def __init__(self, player, companions, world_tone):
        self.player = player
        self.companions = companions
        self.world_tone = world_tone
        self.story_manager = CombatStoryManager(player, companions, world_tone)

    def generate_combat_choices(self):
        return [
            "Charge forward aggressively",
            "Use the environment to your advantage",
            "Stall and buy time",
            "Outwit the enemy with a trick",
            "Brace for impact and endure"
        ]

    def resolve_choice(self, choice_index):
        # --- Randomize battle outcome ---
        roll = random.randint(1, 100)

        if roll >= 60:
            success = True
        else:
            success = False

        # --- Get dynamic combat story ---
        narrative, scar_text, instinct_text = self.story_manager.generate_combat_result(choice_index, success)

        return narrative, scar_text, instinct_text
