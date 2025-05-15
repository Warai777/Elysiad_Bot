class Container:
    def __init__(self, name, type_, slots, dimensions):
        self.name = name
        self.type = type_  # e.g., backpack, ring
        self.slots = slots
        self.items = []
        self.dimensions = dimensions  # dict with length, width, height, unit

    def is_full(self):
        return len(self.items) >= self.slots

    def volume_capacity(self):
        d = self.dimensions
        if d["unit"] == "in":
            return d["length"] * d["width"] * d["height"]
        # Add other unit conversions as needed
        return 0

    def volume_used(self):
        total = 0
        for item in self.items:
            dim = item.get("dimensions", {})
            if dim.get("unit") == "in":
                total += dim.get("length", 0) * dim.get("width", 0) * dim.get("height", 0)
        return total

    def fits(self, item):
        if self.is_full():
            return False
        if item.get("dimensions", {}).get("unit") != self.dimensions.get("unit"):
            return False
        return self.volume_used() + (item["dimensions"]["length"] * item["dimensions"]["width"] * item["dimensions"]["height"]) <= self.volume_capacity()

    def add_item(self, item):
        if self.fits(item):
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
            "items": self.items,
            "dimensions": self.dimensions
        }

    @staticmethod
    def from_dict(data):
        c = Container(data["name"], data["type"], data["slots"], data["dimensions"])
        c.items = data.get("items", [])
        return c