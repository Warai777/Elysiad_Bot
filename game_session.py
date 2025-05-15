from container import Container
from datetime import datetime
from flask import session

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
        self.npc_memory = {}
        self.action_history = []  # major player choices

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
            "containers": [c.to_dict() for c in self.containers],
            "npc_memory": self.npc_memory,
            "action_history": self.action_history
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
        self.npc_memory = data.get("npc_memory", {})
        self.action_history = data.get("action_history", [])

    def autosave(self):
        from routes.save_routes import save_slots
        slot_name = session.get("active_slot")
        user_id = session.get("user")
        if user_id and slot_name:
            if user_id not in save_slots:
                save_slots[user_id] = {}
            save_slots[user_id][slot_name] = self.to_dict()

    def log_action(self, description, consequence=""):
        self.action_history.append({
            "description": description,
            "consequence": consequence,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.autosave()

    def get_total_weight(self):
        return sum(i.get("weight", 0) for i in self.inventory)

    def total_container_volume_used(self):
        return sum(c.volume_used() for c in self.containers)

    def can_carry(self, weight):
        return self.get_total_weight() + weight <= self.strength * 5

    def add_item(self, item):
        if self.can_carry(item.get("weight", 0)):
            self.inventory.append(item)
            self.autosave()
            return True
        return False

    def log_journal(self, text, type_="system", importance="medium", tags=None):
        self.journal.append({
            "text": text,
            "type": type_,
            "importance": importance,
            "tags": tags or [],
            "timestamp": datetime.utcnow().isoformat()
        })
        self.autosave()

    def log_lore(self, text):
        self.log_journal(text, type_="lore", importance="high", tags=["lore"])

    def log_combat(self, text):
        self.log_journal(text, type_="combat", importance="medium", tags=["combat"])

    def log_custom_note(self, text):
        self.log_journal(text, type_="note", importance="low", tags=["custom"])

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
                    self.log_lore(f"You deciphered {i['name']} — once veiled as '{old_name}'")
        if revealed:
            self.autosave()
        return revealed

    def update_npc_memory(self, npc, event, suspicion_delta=0):
        if npc not in self.npc_memory:
            self.npc_memory[npc] = {"suspicion": 0, "memories": []}
        self.npc_memory[npc]["suspicion"] += suspicion_delta
        self.npc_memory[npc]["memories"].append(event)
        self.log_journal(f"{npc} remembers: {event} (Suspicion now {self.npc_memory[npc]['suspicion']})", type_="system", importance="medium", tags=["npc"])
        self.autosave()