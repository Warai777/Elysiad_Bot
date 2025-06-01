# lore_tracker.py

class LoreFragment:
    def __init__(self, fragment_id, title, text, tags=None, origin_world=None, discovery_method=None):
        self.id = fragment_id
        self.title = title
        self.text = text
        self.tags = tags or []
        self.origin_world = origin_world
        self.discovery_method = discovery_method

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "tags": self.tags,
            "origin_world": self.origin_world,
            "discovery_method": self.discovery_method
        }

    @staticmethod
    def from_dict(data):
        return LoreFragment(
            fragment_id=data["id"],
            title=data["title"],
            text=data["text"],
            tags=data.get("tags", []),
            origin_world=data.get("origin_world"),
            discovery_method=data.get("discovery_method")
        )

class LoreTracker:
    def __init__(self):
        self.unlocked_fragments = {}

    def unlock(self, fragment: LoreFragment):
        self.unlocked_fragments[fragment.id] = fragment

    def is_unlocked(self, fragment_id):
        return fragment_id in self.unlocked_fragments

    def get_all_unlocked(self):
        return list(self.unlocked_fragments.values())

    def to_dict(self):
        return {fid: frag.to_dict() for fid, frag in self.unlocked_fragments.items()}

    @staticmethod
    def from_dict(data):
        tracker = LoreTracker()
        for fid, frag_data in data.items():
            tracker.unlocked_fragments[fid] = LoreFragment.from_dict(frag_data)
        return tracker