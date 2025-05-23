import random

def generate_emporium_items(category, tier):
    if category != "Techniques":
        return []

    db = {
        "10-C": [
            {
                "name": "Steel Palm Technique",
                "description": "Beginner martial art focusing force into a single blow.",
                "tier": "10-C", "cost": 90, "original_origin": "Generic Martial World",
                "requires_mastery": False,
                "translation_examples": {
                    "Harry Potter": "Palm-thrust charm with spell channeling.",
                    "Cyberpunk": "Shock glove mod embedded in a training rig.",
                    "Naruto": "Basic academy taijutsu move."
                }
            }
        ],
        "10-B": [
            {
                "name": "Red Tiger Fang",
                "description": "An elite melee style with explosive counters and feints.",
                "tier": "10-B", "cost": 130, "original_origin": "Red Cliff Chronicles",
                "requires_mastery": True,
                "translation_examples": {
                    "Cyberpunk": "Exosuit-enhanced combo modules.",
                    "Naruto": "Taijutsu form requiring chakra precision."
                }
            }
        ],
        "10-A": [
            {
                "name": "Iron Spirit Kata",
                "description": "Peak human stance combining focus, breath, and inner force.",
                "tier": "10-A", "cost": 180, "original_origin": "Samurai Dharma",
                "requires_mastery": True,
                "translation_examples": {
                    "Bleach": "A form of spiritual grounding used in Zanjutsu.",
                    "LOTR": "Elven warrior breath technique fused with sword flow."
                }
            }
        ],
        "9-C": [
            {
                "name": "Fury Chain Style",
                "description": "Unleashes rapid wall-shattering chained blows.",
                "tier": "9-C", "cost": 240, "original_origin": "Beastfist Arena",
                "requires_mastery": True,
                "translation_examples": {
                    "Attack on Titan": "Omni-directional strike loop in close quarters.",
                    "Cyberpunk": "Servo-accelerated chainstrike system."
                }
            }
        ],
        "0": [
            {
                "name": "Conceptual Edge - Type: Null",
                "description": "A technique that unravels anything with a defined form or purpose.",
                "tier": "0", "cost": 9999, "original_origin": "Outervoid Archives",
                "requires_mastery": True,
                "translation_examples": {
                    "Naruto": "Ninjutsu negation slash able to delete intent itself.",
                    "Harry Potter": "Curse beyond Unforgivable class — tears reality's 'why'.",
                    "Cyberpunk": "Null-logic blade hack that makes targets un-code."
                }
            }
        ]
    }

    return db.get(tier, [])