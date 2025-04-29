import random
from procedural_companion_generator import ProceduralCompanionGenerator
from flask import session

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

class CompanionManager:
    def __init__(self):
        pass

    def generate_ability_from_archetype(self, archetype):
        templates = {
            "Mystic Trickster": {"name": "Illusion Step", "description": "Flicker between realities to dodge death once."},
            "Spirit Whisperer": {"name": "Soul Tether", "description": "Bind fate to one ally, saving them once."},
            "Dreamwalker": {"name": "Ethereal Passage", "description": "Walk through danger unseen once per world."},
            "Vengeful Flame": {"name": "Burning Vow", "description": "Upon ally death, gain massive attack boost."},
            "Death Knight": {"name": "Last Stand", "description": "Revives for one final attack after falling."},
            "Umbra Chain": {"name": "Shadow Bind", "description": "Snare a random enemy option, locking it temporarily."},
            "Starforged Guardian": {"name": "Meteor Shield", "description": "Nullify the next deadly hit from cosmic forces."},
            "Dimensional Rift": {"name": "Space Tear", "description": "Create an escape portal once per world."},
            "Aether Pulse": {"name": "Fate Reroll", "description": "Re-roll one death choice per chapter."},
            "Wild Instinct": {"name": "Beast's Frenzy", "description": "Attack wildly, overwhelming a foe."},
            "Storm Rider": {"name": "Lightning Dash", "description": "Evade one fatal choice by storm speed."},
            "Scout Vanguard": {"name": "First Strike", "description": "Attack first when danger is sensed."},
            "Silent Step": {"name": "Ghost Walk", "description": "Bypass one death option quietly."},
            "Faded Memory": {"name": "Remembrance", "description": "Persist through death once by memory strength."},
            "Broken Warden": {"name": "Defiant Wall", "description": "Massive defense bonus when loyalty is high."},
            "Shieldbearer": {"name": "Guardian Oath", "description": "Boost defense of all allies nearby."},
            "Braveheart": {"name": "Courage Surge", "description": "Boost chance of surviving impossible odds."},
            "Sword of Dawn": {"name": "Final Eclipse", "description": "Deal massive damage during climactic events."},
            "Foresight Pulse": {"name": "Glimpse of Doom", "description": "See the death choice subtly before picking."},
            "Veil Step": {"name": "Slipstream", "description": "Reverse one wrong choice after choosing."},
            "Cursed Insight": {"name": "Dreadful Knowledge", "description": "Unlock a hidden, dark path."},
            "Soul Guard": {"name": "Soul Sacrifice", "description": "Take fatal blow instead of ally."},
            "Wandering Light": {"name": "Hope's Beacon", "description": "Prevent despair events once."},
            "Echo Pilgrim": {"name": "Resonance Walk", "description": "Boost success chance if loyalty is high."},
            "Dream Threader": {"name": "Weave Fate", "description": "Reshape a bad ending once."},
            "Reality Breaker": {"name": "Anomaly", "description": "Cause unexpected positive random events."},
            "Flickering Muse": {"name": "Inspire Madness", "description": "Confuse enemies (randomizes death/life chance)."}
        }
        return templates.get(archetype, {"name": "Unknown Spark", "description": "A mysterious ability yet to awaken."})

    def random_companion_encounter(self):
        if random.random() < 0.25:
            current_tone = session.get("current_world_tone", "mystical")  # fallback if none

            possible_archetypes = TONE_ARCHETYPE_MAP.get(current_tone, ["Wild Instinct"])
            chosen_archetype = random.choice(possible_archetypes)
            ability = self.generate_ability_from_archetype(chosen_archetype)

            companion = {
                "name": random.choice(["Vaerin", "Lune", "Korr", "Asha", "Nilo", "Thorn", "Zerik", "Lyra", "Sorin"]),
                "type": random.choice(["Assault", "Support", "Scout", "Mystic"]),
                "traits": random.sample(["Loyal", "Proud", "Calm", "Impulsive", "Watchful", "Clever"], 2),
                "special_trait": random.choice(["Adaptive", "Soul-Synced", "Veteran", "Empath", "Unstable"]),
                "base_hp": random.randint(30, 80),
                "attack": random.randint(5, 20),
                "defense": random.randint(5, 20),
                "loyalty": 50,
                "archetype": chosen_archetype,
                "ability": ability,
                "memories": []
            }

            return companion
        return None
