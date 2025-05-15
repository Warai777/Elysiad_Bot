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

    def reveal_items(self):
        revealed = []
        for i in self.inventory:
            if i.get("type") == "mystery":
                r = i["requirements"]
                if (
                    self.strength >= r.get("strength", 0)
                    and all(trait in self.traits for trait in r.get("traits", []))
                    and (not r.get("roles") or any(role in self.roles for role in r["roles"]))
                ):
                    i["name"] = i.pop("true_name")
                    i["description"] = i.pop("true_description")
                    i["effect"] = i.pop("true_effect")
                    i["type"] = "revealed"
                    revealed.append(i["name"])
        return revealed