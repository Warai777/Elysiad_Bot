import random
import json
import os
from datetime import datetime
from container import Container

class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.name = ""
        self.inventory = []
        self.containers = []
        self.journal = []
        self.lore = []
        self.phase = "Intro"
        self.current_phase = "Intro"
        self.current_world = ""
        self.strength = 5
        self.traits = []
        self.roles = []
        self.suspicion = 0
        self.missions = []
        self.chapter_titles = []
        self.chapters = []
        self.current_chapter_index = 0
        self.current_chapter_id = None

    def start_chapter(self, title):
        chapter = {
            "id": len(self.chapters) + 1,
            "title": title,
            "timestamp": datetime.utcnow().isoformat(),
            "content": []
        }
        self.chapters.append(chapter)
        self.current_chapter_index = len(self.chapters) - 1
        self.current_chapter_id = chapter["id"]
        self.log_journal(f"-- {title} begins --", type_="system", importance="high", tags=["chapter"])

    def log_journal(self, text, type_="narrative", importance="normal", tags=None):
        entry = {
            "text": text,
            "type": type_,
            "importance": importance,
            "tags": tags or [],
            "timestamp": datetime.utcnow().isoformat()
        }
        self.journal.append(entry)
        if self.chapters:
            self.chapters[self.current_chapter_index]["content"].append(entry)

    def log_custom_note(self, note):
        self.log_journal(note, type_="note", importance="normal", tags=["user"])

    def autosave_if_needed(self):
        save_dir = "data/saves"
        os.makedirs(save_dir, exist_ok=True)
        data = {
            "name": self.name,
            "inventory": self.inventory,
            "containers": [c.to_dict() for c in self.containers],
            "journal": self.journal,
            "lore": self.lore,
            "phase": self.phase,
            "world": self.current_world,
            "strength": self.strength,
            "traits": self.traits,
            "roles": self.roles,
            "chapters": self.chapters
        }
        with open(f"{save_dir}/{self.session_id}_autosave.json", "w") as f:
            json.dump(data, f, indent=2)

    def reveal_items(self):
        revealed = []
        for item in self.inventory:
            if item.get("type") == "mystery" and self.strength >= item.get("requirements", {}).get("strength", 0):
                item["type"] = "revealed"
                item["description"] = item.get("true_description", "")
                item["effect"] = item.get("true_effect", "")
                revealed.append(item["name"])
        return revealed