import random

def generate_emporium_items(category, tier):
    db = {
        "Techniques": {
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
        },
        "Relics & Artifacts": {
            "10-C": [
                {
                    "name": "Bone Charm of Stillness",
                    "description": "Suppresses movement sound, favored by novice thieves.",
                    "tier": "10-C", "cost": 85, "original_origin": "Dishonored",
                    "requires_mastery": False,
                    "translation_examples": {
                        "Harry Potter": "An amulet with silencing charm.",
                        "Cyberpunk": "Magno-silencer chip for boots.",
                        "Naruto": "Quiet movement fuuinjutsu seal."
                    }
                }
            ],
            "10-B": [
                {
                    "name": "Hollowblade Shard",
                    "description": "Shattered blade that pulses in the hands of killers.",
                    "tier": "10-B", "cost": 145, "original_origin": "Bloodbornian Depths",
                    "requires_mastery": True,
                    "translation_examples": {
                        "LOTR": "Cursed dagger fragment lost in Mirkwood.",
                        "Cyberpunk": "Smartblade relic with encoded kill-count."
                    }
                }
            ],
            "9-C": [
                {
                    "name": "Stonelash Totem",
                    "description": "Unleashes a burst strong enough to crack barricades.",
                    "tier": "9-C", "cost": 250, "original_origin": "Tribal Ascension",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Naruto": "Summons an earth chakra spike wave.",
                        "Cyberpunk": "Concrete-shattering sonic mine."
                    }
                }
            ],
            "0": [
                {
                    "name": "Relic of the Last Dream",
                    "description": "Grants insight into realities that never were.",
                    "tier": "0", "cost": 8888, "original_origin": "Sleepwalk Continuum",
                    "requires_mastery": True,
                    "translation_examples": {
                        "LOTR": "Palantír shard that reveals what should have been.",
                        "Cyberpunk": "Brain relic that plays neural ghost futures."
                    }
                }
            ]
        },
        "Tomes & Knowledge": {
            "10-C": [
                {
                    "name": "Beginner Hex Scroll",
                    "description": "Contains entry-level binding and sensory curses.",
                    "tier": "10-C", "cost": 70, "original_origin": "Witchschool Archives",
                    "requires_mastery": False,
                    "translation_examples": {
                        "Naruto": "Paralysis seal formula with tracing chakra thread.",
                        "Cyberpunk": "Basic surveillance hack notes."
                    }
                }
            ],
            "10-B": [
                {
                    "name": "Scripture of Internal Flame",
                    "description": "Teaches will-fueled ignition techniques.",
                    "tier": "10-B", "cost": 120, "original_origin": "Flarehand Monks",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Harry Potter": "Wandless firecraft rituals.",
                        "Naruto": "Scroll of inner chakra combustion."
                    }
                }
            ],
            "9-C": [
                {
                    "name": "Codex of Force Locks",
                    "description": "Explains how to compress force into magical glyphs.",
                    "tier": "9-C", "cost": 200, "original_origin": "Runebreak Keep",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Cyberpunk": "Manual for compression grenades with sigil seals.",
                        "Naruto": "Exploding seal tuning guide."
                    }
                }
            ],
            "0": [
                {
                    "name": "The Whispering Index",
                    "description": "A book that updates itself with cosmic truths from all timelines.",
                    "tier": "0", "cost": 7777, "original_origin": "The Dream Librarium",
                    "requires_mastery": True,
                    "translation_examples": {
                        "Harry Potter": "Uncatalogued tome from the Room of Requirement.",
                        "Cyberpunk": "AI script that writes forbidden prophecy logs."
                    }
                }
            ]
        }
    }

    return db.get(category, {}).get(tier, [])