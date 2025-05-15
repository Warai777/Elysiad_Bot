import random

def generate_item(action_text, session):
    # Basic templates based on action context
    templates = [
        {
            "name": "Burned Map Fragment",
            "description": "A half-charred scrap showing cryptic paths. Faint heat still radiates.",
            "weight": 2,
            "type": "clue",
            "effect": "map_reveal",
            "requirements": []
        },
        {
            "name": "Shimmering Lens",
            "description": "Reveals hidden glyphs when held to moonlight.",
            "weight": 1,
            "type": "tool",
            "effect": "reveal_glyph",
            "requirements": []
        },
        {
            "name": "Coal-etched Coin",
            "description": "Used by dream merchants. Holding it whispers questions in your ear.",
            "weight": 1,
            "type": "currency",
            "effect": "dream_trigger",
            "requirements": ["dream_resistance"]
        },
        {
            "name": "Spirit-locked Scroll",
            "description": "A sealed scroll that burns any unworthy hand.",
            "weight": 3,
            "type": "scroll",
            "effect": "vision_spell",
            "requirements": ["fire_affinity"]
        }
    ]

    # Match template randomly or based on traits
    eligible = []
    for t in templates:
        if all(req in session.traits for req in t["requirements"]):
            eligible.append(t)

    return random.choice(eligible or templates)