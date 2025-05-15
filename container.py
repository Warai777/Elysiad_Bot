class Container:
    def __init__(self, name, type_, slots):
        self.name = name
        self.type = type_  # e.g., backpack, ring
        self.slots = slots
        self.items = []

    def is_full(self):
        return len(self.items) >= self.slots

    def add_item(self, item):
        if not self.is_full():
            self.items.append(item)
            return True
        return False

    def remove_item(self, item_name):
        for i in self.items:
            if i["name"] == item_name:
                self.items.remove(i)
                return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "slots": self.slots,
            "items": self.items
        }

    @staticmethod
    def from_dict(data):
        c = Container(data["name"], data["type"], data["slots"])
        c.items = data.get("items", [])
        return c