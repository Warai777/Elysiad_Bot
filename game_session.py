from container import Container

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
        self.containers = [
            Container("Pockets", "starter", 2, {"length": 6, "width": 4, "height": 0.75, "unit": "in"})
        ]

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
            "containers": [c.to_dict() for c in self.containers]
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
        self.containers = [Container.from_dict(c) for c in data.get("containers", [])]

    def get_total_weight(self):
        return sum(i.get("weight", 0) for i in self.inventory)

    def total_container_volume_used(self):
        return sum(c.volume_used() for c in self.containers)

    def can_carry(self, weight):
        return self.get_total_weight() + weight <= self.strength * 5

    def add_item(self, item):
        if self.can_carry(item.get("weight", 0)):
            self.inventory.append(item)
            return True
        return False

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
                    old_name = i["name"]
                    i["name"] = i.pop("true_name")
                    i["description"] = i.pop("true_description")
                    i["effect"] = i.pop("true_effect")
                    i["type"] = "revealed"
                    revealed.append(i["name"])
                    self.journal.append(f"You deciphered {i['name']} — once veiled as '{old_name}'")
        return revealed