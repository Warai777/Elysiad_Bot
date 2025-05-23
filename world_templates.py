import random

def generate_ai_world_template(tier="10-C"):
    sample_worlds = {
        "10-C": [
            {
                "name": "Frosthollow",
                "summary": "A bleak village where rumors of frost spirits cause strange disappearances.",
                "tone": "Survival mystery",
                "canon_profile": {"name": "Mira Holloway", "role": "Warden's daughter"},
                "inspiration": "Original", "tier": "10-C"
            }
        ],
        "10-B": [
            {
                "name": "Ashspire",
                "summary": "An empire built atop lava rivers wages war with flame-bound titans.",
                "tone": "Military high-fantasy",
                "canon_profile": {"name": "Ser Darius", "role": "Knight-Commander"},
                "inspiration": "Original", "tier": "10-B"
            }
        ],
        "9-C": [
            {
                "name": "Thorneveil",
                "summary": "A cursed city where beasts roam the rooftops and law is enforced with arcane whips.",
                "tone": "Gothic horror",
                "canon_profile": {"name": "Inspector Vell", "role": "Rune Enforcer"},
                "inspiration": "Bloodborne-inspired", "tier": "9-C"
            }
        ],
        "0": [
            {
                "name": "The Echo Beyond Void",
                "summary": "A non-space where reality loops and identity splinters against the Archivist’s forbidden glyphs.",
                "tone": "Cosmic metafiction",
                "canon_profile": {"name": "The One Who Remembers", "role": "Echo Anchor"},
                "inspiration": "Dream-World: Elysiad Root", "tier": "0"
            }
        ]
    }
    return random.choice(sample_worlds.get(tier, sample_worlds["10-C"]))