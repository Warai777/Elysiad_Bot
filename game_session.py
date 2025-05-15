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
        self.action_history = []
        self.chapters = []
        self.current_chapter_index = -1
        self.start_chapter("Prologue: Your Arrival")

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
            "action_history": self.action_history,
            "chapters": self.chapters,
            "current_chapter_index": self.current_chapter_index
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
        self.chapters = data.get("chapters", [])
        self.current_chapter_index = data.get("current_chapter_index", -1)

    def start_chapter(self, title):
        self.chapters.append({
            "title": title,
            "timestamp": datetime.utcnow().isoformat(),
            "tags": [],
            "content": []
        })
        self.current_chapter_index = len(self.chapters) - 1
        self.autosave()

    def append_to_chapter(self, text):
        if self.current_chapter_index >= 0:
            self.chapters[self.current_chapter_index]["content"].append(text)
            self.autosave()

    def autosave(self):
        from routes.save_routes import save_slots
        slot_name = session.get("active_slot")
        user_id = session.get("user")
        if user_id and slot_name:
            if user_id not in save_slots:
                save_slots[user_id] = {}
            save_slots[user_id][slot_name] = self.to_dict()

    # ... other methods unchanged ...