import random

def generate_emporium_items(category, tier):
    db = {
        "Techniques": {
            "10-C": [...],
            "10-B": [...],
            "9-C": [...],
            "0": [...]
        },
        "Relics & Artifacts": {
            "10-C": [...],
            "10-B": [...],
            "9-C": [...],
            "0": [...]
        },
        "Tomes & Knowledge": {
            "10-C": [...],
            "10-B": [...],
            "9-C": [...],
            "0": [...]
        },
        "Essences & Cores": {
            "10-C": [
                {
                    "name": "Ember Root",
                    "description": "A weak but volatile elemental node, found in volcanic gardens.",
                    "tier": "10-C", "cost": 60, "original_origin": "Element Scrolls",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Naruto": "Seed of fire chakra that awakens with breath control.",
                        "Cyberpunk": "Biochip enzyme fuse that triggers warmth surge."
                    }
                }
            ],
            "0": [
                {
                    "name": "Heart of Null Flame",
                    "description": "An essence that consumes form, identity, and purpose.",
                    "tier": "0", "cost": 7777, "original_origin": "Metavortex Saga",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Harry Potter": "Elder Essence forbidden even in magical law.",
                        "Cyberpunk": "An AI anomaly that redacts existence."
                    }
                }
            ]
        },
        "Titles & Blessings": {
            "10-C": [
                {
                    "name": "Novice of the Wandering Flame",
                    "description": "Slightly increases endurance and reduces fear.",
                    "tier": "10-C", "cost": 50, "original_origin": "Pilgrims of Ash",
                    "requires_mastery": False,
                    "translation_examples": {
                        "Naruto": "Sage path recognition aura.",
                        "Cyberpunk": "Cortical upgrade that mutes dread response."
                    }
                }
            ],
            "0": [
                {
                    "name": "Bearer of the Inverted Halo",
                    "description": "You exist outside fate. Cannot be predicted.",
                    "tier": "0", "cost": 10000, "original_origin": "Book of Paradox",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Harry Potter": "Untraceable, immune to prophecy magic.",
                        "Cyberpunk": "Quantum entropy ghost."
                    }
                }
            ]
        },
        "Summons & Contracts": {
            "10-C": [
                {
                    "name": "Pact of the Ember Wisp",
                    "description": "Summons a small flame sprite to illuminate and warm.",
                    "tier": "10-C", "cost": 75, "original_origin": "Candlespire Tales",
                    "requires_mastery": False,
                    "translation_examples": {
                        "Naruto": "Fire summon jutsu for minor flame fox.",
                        "Cyberpunk": "Mini drone with biothermal lamp."
                    }
                }
            ],
            "0": [
                {
                    "name": "Contract of the Last Maw",
                    "description": "Summons a hunger that devours memory, language, and form.",
                    "tier": "0", "cost": 9999, "original_origin": "Howlers Beyond Ends",
                    "requires_mastery": True,
                    "translation_examples": {
                        "LOTR": "A void beast sealed beyond the Grey Havens.",
                        "Cyberpunk": "Black AI blob that eats digital consciousness."
                    }
                }
            ]
        }
    }

    return db.get(category, {}).get(tier, [])