# lore_tracker.py

class LoreTracker:
    def __init__(self):
        self.unlocked_fragments = set()

    def unlock(self, fragment_id):
        self.unlocked_fragments.add(fragment_id)

    def is_unlocked(self, fragment_id):
        return fragment_id in self.unlocked_fragments

    def get_all_unlocked(self):
        return list(self.unlocked_fragments)