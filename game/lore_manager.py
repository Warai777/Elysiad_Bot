class LoreManager:
    def __init__(self):
        self.lore_registry = []  # [{"text": ..., "phase": ..., "tags": [...], "branch_key": ..., "secret": bool}]

    def register_lore(self, text, phase="Exploration", tags=None, branch_key=None, secret=False):
        self.lore_registry.append({
            "text": text,
            "phase": phase,
            "tags": tags or [],
            "branch_key": branch_key,
            "secret": secret
        })

    def get_lore_for_phase(self, current_phase):
        return [l["text"] for l in self.lore_registry if l["phase"] == current_phase and not l["secret"]]

    def get_lore_by_tag(self, tag):
        return [l["text"] for l in self.lore_registry if tag in l.get("tags", []) and not l["secret"]]

    def get_hidden_lore(self, branch_keys):
        return [l["text"] for l in self.lore_registry if l.get("secret") and l.get("branch_key") in branch_keys]