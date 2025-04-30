import random

class CombatManager:
    def __init__(self, player, companions, tone="neutral"):
        self.player = player
        self.companions = companions
        self.tone = tone
        self.scars = ["a deep gash", "a burned mark", "a psychic wound", "a lost memory"]
        self.instincts = ["dodge", "block", "counter", "channel power"]

    def generate_combat_choices(self):
        return [
            "Strike quickly",
            "Defend and wait",
            "Unleash a risky technique",
            "Look for an escape",
            "Call out to your companion"
        ]

    def resolve_choice(self, selected_index):
        result = {
            "narrative": "",
            "scar_text": "",
            "instinct_text": "",
            "assist_text": ""
        }

        # Outcome logic based on player choice
        if selected_index == 0:
            result["narrative"] = "You lunge forward with raw aggression, catching the enemy off guard."
        elif selected_index == 1:
            result["narrative"] = "You brace yourself and let the enemy strike first. You read their rhythm."
        elif selected_index == 2:
            result["narrative"] = "You burn energy and focus into a powerful—but unstable—technique."
        elif selected_index == 3:
            result["narrative"] = "Your eyes scan for a weak point in the terrain. You find an exit."
        elif selected_index == 4:
            result["narrative"] = "You call to your companion—and something answers."

        # Scar system (20% chance)
        if random.random() < 0.2:
            result["scar_text"] = f"You suffer {random.choice(self.scars)} during the encounter."

        # Instinct system (30% chance)
        if random.random() < 0.3:
            result["instinct_text"] = f"An instinct surges—you {random.choice(self.instincts)} just in time."

        # Companion assist system
        assist_candidates = [c for c in self.companions if c.get("loyalty", 0) >= 75]
        if assist_candidates and random.random() < 0.5:
            comp = random.choice(assist_candidates)
            result["assist_text"] = f"{comp['name']} steps in! They use {comp['ability']['name']} to support you."

        return result["narrative"], result["scar_text"], result["instinct_text"], result["assist_text"]
