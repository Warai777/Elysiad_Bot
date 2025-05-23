import random

def generate_emporium_items(category, tier):
    # Simple fictional seeds (to be replaced with AI-backed logic later)
    techniques_10C = [
        {
            "name": "Steel Palm Technique",
            "description": "A beginner martial art that channels strength into a single focused strike.",
            "tier": "10-C",
            "cost": 90,
            "original_origin": "Generic Martial World",
            "requires_mastery": False,
            "translation_examples": {
                "Harry Potter": "Palm-thrust charm augmented by body channeling spells.",
                "Cyberpunk": "Palm-mounted shock mod embedded in a neural glove.",
                "Naruto": "A basic taijutsu move taught in academy sparring."
            }
        },
        {
            "name": "Echo Blade Form I",
            "description": "A basic stance used to deliver quick slashing attacks that leave sonic trails.",
            "tier": "10-C",
            "cost": 110,
            "original_origin": "Soundverse Chronicles",
            "requires_mastery": True,
            "translation_examples": {
                "Harry Potter": "A charm that makes slashes audible and disorienting.",
                "Cyberpunk": "Sonic-edged vibroblade technique.",
                "Naruto": "Swordplay combined with Sound Village jutsu."
            }
        }
    ]

    if category == "Techniques" and tier == "10-C":
        return random.sample(techniques_10C, k=len(techniques_10C))
    return []