class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.origin_essence = 0
        self.suspicion = 0
        self.year = 0
        self.inventory = []  # on-body items only
        self.journal = []
        self.unlocked_lore = []
        self.tier = 0
        self.traits = ["basic_strength"]  # default trait
        self.strength = 5  # determines carry weight
        self.containers = []  # backpack, ring, suitcase etc.

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "origin_essence": self.origin_essence,
            "suspicion": self.suspicion,
            "year": self.year,
            "inventory": self.inventory,
            "journal": self.journal,
            "unlocked_lore": self.unlocked_lore,
            "tier": self.tier,
            "traits": self.traits,
            "strength": self.strength,
            "containers": self.containers
        }

    def load_from_dict(self, data):
        self.origin_essence = data.get("origin_essence", 0)
        self.suspicion = data.get("suspicion", 0)
        self.year = data.get("year", 0)
        self.inventory = data.get("inventory", [])
        self.journal = data.get("journal", [])
        self.unlocked_lore = data.get("unlocked_lore", [])
        self.tier = data.get("tier", 0)
        self.traits = data.get("traits", ["basic_strength"])
        self.strength = data.get("strength", 5)
        self.containers = data.get("containers", [])