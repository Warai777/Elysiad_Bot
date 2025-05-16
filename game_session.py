...TRUNCATED...

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
        self.current_world = data.get("current_world", None)

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
            "current_chapter_index": self.current_chapter_index,
            "current_world": self.current_world
        }

    def enter_new_world(self, world_name):
        self.current_world = world_name
        self.start_chapter(f"Chapter {len(self.chapters)+1}: {world_name} Begins")
        self.log_journal(f"You have entered the world of {world_name}.", type_="system")
        self.autosave()

...TRUNCATED...