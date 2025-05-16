class Container:
    def __init__(self, name, type_, slots, dimensions, special_requirements=None):
        self.name = name
        self.type = type_  # e.g., backpack, ring
        self.slots = slots
        self.items = []
        self.dimensions = dimensions  # dict with length, width, height, unit
        self.special_requirements = special_requirements or {}  # traits, roles, strength

    def is_full(self):
        return len(self.items) >= self.slots

    def normalize_volume(self, length, width, height, unit):
        unit = unit.lower()
        factor = {
            "in": 1,
            "cm": 0.0610237,
            "m": 61023.7,
            "ft": 1728,
            "km": 61023700000,
            "mi": 2688000000
        }.get(unit, 1)  # fallback to inches
        return length * width * height * factor

    def volume_capacity(self):
        d = self.dimensions
        return self.normalize_volume(d["length"], d["width"], d["height"], d["unit"])

    def volume_used(self):
        total = 0
        for item in self.items:
            dim = item.get("dimensions", {})
            total += self.normalize_volume(dim.get("length", 0), dim.get("width", 0), dim.get("height", 0), dim.get("unit", "in"))
        return total

    def fits(self, item):
        if self.is_full():
            return False
        dim = item.get("dimensions", {})
        item_vol = self.normalize_volume(dim.get("length", 0), dim.get("width", 0), dim.get("height", 0), dim.get("unit", "in"))
        return self.volume_used() + item_vol <= self.volume_capacity()

    def access_granted(self, session):
        r = self.special_requirements
        return (
            session.strength >= r.get("strength", 0)
            and all(trait in session.traits for trait in r.get("traits", []))
            and (not r.get("roles") or any(role in session.roles for role in r["roles"]))
        )

    def add_item(self, item):
        if self.fits(item):
            if item.get("type") == "container":
                item.setdefault("linked_items", [])  # Support nested container logic
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
            "dimensions": self.dimensions,
            "special_requirements": self.special_requirements
        }

    @staticmethod
    def from_dict(data):
        c = Container(data["name"], data["type"], data["slots"], data["dimensions"], data.get("special_requirements", {}))
        c.items = data.get("items", [])
        return c