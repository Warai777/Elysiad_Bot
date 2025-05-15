class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.origin_essence = 0
        self.suspicion = 0
        self.year = 0
        self.inventory = []
        self.tier = 0
        self.choice_log = []
        self.unlocked_lore = []
        self.journal = []

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "origin_essence": self.origin_essence,
            "suspicion": self.suspicion,
            "year": self.year,
            "inventory": self.inventory,
            "tier": self.tier,
            "choice_log": self.choice_log,
            "unlocked_lore": self.unlocked_lore,
            "journal": self.journal
        }

    def load_from_dict(self, data):
        self.origin_essence = data.get("origin_essence", 0)
        self.suspicion = data.get("suspicion", 0)
        self.year = data.get("year", 0)
        self.inventory = data.get("inventory", [])
        self.tier = data.get("tier", 0)
        self.choice_log = data.get("choice_log", [])
        self.unlocked_lore = data.get("unlocked_lore", [])
        self.journal = data.get("journal", [])