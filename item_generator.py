import random

def generate_item(action_text, session):
    templates = [
        {
            "name": "Blood-Touched Lens",
            "description": "Magnifies ritual ink. Burns non-initiates.",
            "weight": 2,
            "type": "tool",
            "effect": "glyph_reveal",
            "requirements": {
                "strength": 2,
                "traits": ["ritual_scholar"],
                "roles": []
            }
        },
        {
            "name": "Flame-Etched Coin",
            "description": "Hot to the touch. You hear whispers from the flame.",
            "weight": 1,
            "type": "currency",
            "effect": "fire_whisper",
            "requirements": {
                "strength": 1,
                "traits": ["fire_affinity"],
                "roles": []
            }
        },
        {
            "name": "Dreamroot Vial",
            "description": "Causes lucid visions. Only safe for trained minds.",
            "weight": 1,
            "type": "consumable",
            "effect": "vision_dream",
            "requirements": {
                "strength": 1,
                "traits": ["dream_resistance"],
                "roles": []
            }
        },
        {
            "name": "Archivist’s Thread",
            "description": "Only binds to the Chosen. Emits light when truth is near.",
            "weight": 1,
            "type": "relic",
            "effect": "truth_ping",
            "requirements": {
                "strength": 0,
                "traits": [],
                "roles": ["chosen_one"]
            }
        }
    ]

    def is_valid(item):
        r = item["requirements"]
        return (
            session.strength >= r.get("strength", 0)
            and all(trait in session.traits for trait in r.get("traits", []))
            and (not r.get("roles") or any(role in session.roles for role in r["roles"]))
        )

    item = random.choice(templates)
    if is_valid(item):
        return item
    else:
        return {
            "name": "Unidentified Object",
            "description": "You sense it's not meant for you. It hums faintly in your pack.",
            "weight": item["weight"],
            "type": "mystery",
            "true_name": item["name"],
            "true_description": item["description"],
            "true_effect": item["effect"],
            "requirements": item["requirements"]
        }