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
        self.memory = {
            "Deaths": []
        }
        self.companions = []
        self.grit = 0

        # Transmigration system
        self.host_identity = {
            "name": "Unknown Host",
            "background": "Unknown",
            "personality_traits": []
        }
        self.known_relationships = []  # e.g., ["Mentor: Aizen", "Brother: Tanjiro"]
        self.suspicion_level = 0  # Ranges from 0 (normal) to 100 (exposed)

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
        player.memory = data.get("memory", {"Deaths": []})
        player.companions = data.get("companions", [])
        player.grit = data.get("grit", 0)

        player.host_identity = data.get("host_identity", {
            "name": "Unknown Host",
            "background": "Unknown",
            "personality_traits": []
        })
        player.known_relationships = data.get("known_relationships", [])
        player.suspicion_level = data.get("suspicion_level", 0)

        player.memory.setdefault("Journal", {
            "Hints": [],
            "Lore": [],
            "Events": [],
            "Notes": []
        })

        return player

    def save_now(self):
        self.save()


# --- Loyalty Adjustment Function ---
def adjust_loyalty(player, amount, cause=""):
    for companion in getattr(player, "companions", []):
        if "loyalty" in companion:
            companion["loyalty"] += amount
            companion["loyalty"] = max(0, min(100, companion["loyalty"]))
            if "memories" not in companion:
                companion["memories"] = []
            if cause:
                companion["memories"].append(cause)
    player.save()

def record_memory(player, memory_text):
    for companion in getattr(player, "companions", []):
        if "memories" not in companion:
            companion["memories"] = []
        companion["memories"].append(memory_text)
    player.save()

def kill_companion(player, companion_name):
    dead = None
    for comp in player.companions:
        if comp["name"] == companion_name:
            dead = comp
            break
    if dead:
        player.companions.remove(dead)
        record_memory(player, f"{dead['name']} fell in battle. Their memory haunts you.")
        adjust_loyalty(player, -20, cause=f"Grief from losing {dead['name']}")
        player.save()

# --- Suspicion Adjustment System ---
def adjust_suspicion(player, amount, reason=""):
    player.suspicion_level = max(0, min(100, player.suspicion_level + amount))
    if reason:
        player.memory.setdefault("Journal", {}).setdefault("Events", []).append(
            f"Suspicion raised ({amount}): {reason}"
        )
    if player.suspicion_level >= 100:
        player.memory["Journal"]["Events"].append("You have been fully exposed. The world is turning against you.")
    player.save()
