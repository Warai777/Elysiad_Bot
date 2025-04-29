import random
from procedural_companion_generator import ProceduralCompanionGenerator

class CompanionManager:
    def __init__(self):
        pass  # No need to pre-load fixed companions anymore!

    def random_companion_encounter(self):
        if random.random() < 0.25:  # <-- Correct indentation here!
            abilities = [
                {
                    "name": "Echo Blade",
                    "description": "Once per scene, copies your last attack style as a combo move."
                },
                {
                    "name": "Soul Guard",
                    "description": "Takes the hit for you when your HP would fall below 10%."
                },
                {
                    "name": "Aether Pulse",
                    "description": "Boosts your next choice by fate, rerolling a death outcome once."
                },
                {
                    "name": "Tethered Strike",
                    "description": "Chains an enemy with your attack to weaken their next move."
                },
                {
                    "name": "Silent Step",
                    "description": "Can sneak past one danger choice per world — only once."
                }
            ]

            ability = random.choice(abilities)

            companion = {
                "name": random.choice(["Vaerin", "Lune", "Korr", "Asha", "Nilo", "Thorn"]),
                "type": random.choice(["Assault", "Support", "Scout", "Mystic"]),
                "traits": random.sample(["Loyal", "Proud", "Calm", "Impulsive", "Watchful", "Clever"], 2),
                "special_trait": random.choice(["Adaptive", "Soul-Synced", "Veteran", "Empath", "Unstable"]),
                "base_hp": random.randint(30, 80),
                "attack": random.randint(5, 20),
                "defense": random.randint(5, 20),
                "loyalty": 50,
                "ability": ability
            }
            
            TONE_ARCHETYPE_MAP = {
    "mystical": ["Mystic Trickster", "Spirit Whisperer", "Dreamwalker"],
    "grimdark": ["Vengeful Flame", "Death Knight", "Umbra Chain"],
    "cosmic": ["Starforged Guardian", "Dimensional Rift", "Aether Pulse"],
    "adventurous": ["Wild Instinct", "Storm Rider", "Scout Vanguard"],
    "melancholy": ["Silent Step", "Faded Memory", "Broken Warden"],
    "heroic": ["Shieldbearer", "Braveheart", "Sword of Dawn"],
    "psychological": ["Foresight Pulse", "Veil Step", "Cursed Insight"],
    "spiritual": ["Soul Guard", "Wandering Light", "Echo Pilgrim"],
    "surreal": ["Dream Threader", "Reality Breaker", "Flickering Muse"]
}

            return companion
        return None
