class LoreManager:
    def __init__(self):
        self.lore_registry = []  # [{"text": ..., "phase": ..., "tags": [...]}]

    def register_lore(self, text, phase="Exploration", tags=None):
        self.lore_registry.append({
            "text": text,
            "phase": phase,
            "tags": tags or []
        })

    def get_lore_for_phase(self, current_phase):
        return [l["text"] for l in self.lore_registry if l["phase"] == current_phase]

    def get_lore_by_tag(self, tag):
        return [l["text"] for l in self.lore_registry if tag in l.get("tags", [])]