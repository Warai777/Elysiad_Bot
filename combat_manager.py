import random

class CombatManager:
    def __init__(self, player, companions, world_tone):
        self.player = player
        self.companions = companions
        self.world_tone = world_tone

    def generate_combat_choices(self):
        """Creates 5 unique contextual combat actions."""
        base_actions = [
            "Charge recklessly at the enemy!",
            "Use the environment for an advantage!",
            "Defend and analyze their moves!",
            "Buy time for your companion or ability!",
            "Attempt a daring feint and counter!"
        ]
        random.shuffle(base_actions)
        return base_actions[:5]

    def resolve_choice(self, selected_index):
        """Calculates the result of the selected action."""
        roll = random.randint(1, 100)

        # Adjust difficulty based on world tone
        if self.world_tone in ["grimdark", "cosmic"]:
            roll -= 10
        elif self.world_tone in ["heroic", "adventurous"]:
            roll += 10

        # Companion assistance bonus
        if self.companions:
            roll += random.randint(5, 15)

        outcome = ""
        scar = False
        instinct_gain = False

        if roll >= 80:
            outcome = "Brilliant Success! You outclass the enemy."
            instinct_gain = True
        elif roll >= 50:
            outcome = "You barely succeed but survive the encounter."
        elif roll >= 30:
            outcome = "Partial success — you survive but are scarred mentally."
            scar = True
        else:
            outcome = "Disastrous failure — you are overwhelmed!"
            scar = True

        return outcome, scar, instinct_gain
