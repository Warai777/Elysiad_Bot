import random

def generate_item(context):
    tier = context.get("tier", 0)
    strength = context.get("strength", 5)
    traits = context.get("traits", [])
    phase = context.get("phase", "Intro")

    names = ["Sealed Fang", "Ancient Sigil", "Arcane Coil", "Dusty Lens"]
    descs = [
        "It pulses with forgotten energy.",
        "The markings glow faintly.",
        "You feel a chill pass through your fingers.",
        "It's unnaturally heavy."
    ]

    rarity_tags = ["common", "rare", "epic", "mythic"]
    special_tags = ["fire-bound", "cult-only", "essence-linked", "one-use"]

    base = {
        "name": random.choice(names),
        "description": random.choice(descs),
        "type": "mystery",
        "weight": round(random.uniform(0.2, 5.0), 2),
        "dimensions": {
            "length": random.randint(3, 15),
            "width": random.randint(1, 6),
            "height": random.randint(1, 6),
            "unit": "in"
        },
        "requirements": {
            "strength": strength + random.randint(1, 4),
            "traits": [t for t in traits if random.random() > 0.5],
            "roles": []
        },
        "true_name": "???",
        "true_description": "Still shrouded in secrets.",
        "true_effect": "Unknown phenomenon activates.",
        "rarity": random.choices(rarity_tags, weights=[60, 25, 10, 5])[0],
        "tags": random.sample(special_tags, k=random.randint(0, 2))
    }

    return base