class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.origin_essence = 0
        self.suspicion = 0
        self.year = 0
        self.inventory = []
        self.journal = []
        self.unlocked_lore = []
        self.tier = 0
        self.strength = 5
        self.traits = ["basic_strength"]
        self.roles = []
        self.containers = []

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
            "strength": self.strength,
            "traits": self.traits,
            "roles": self.roles,
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
        self.strength = data.get("strength", 5)
        self.traits = data.get("traits", ["basic_strength"])
        self.roles = data.get("roles", [])
        self.containers = data.get("containers", [])