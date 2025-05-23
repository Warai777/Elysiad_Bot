import random

def generate_ai_world_template(tier="10-C"):
    inspirations = {
        "10-C": ["Slice of Life City", "Medieval Hamlet", "Low-Risk School Life"],
        "10-B": ["Sports Drama Town", "Rural Ninja Village"],
        "10-A": ["Elite Soldier Base", "Haunted Research Lab"],
        "9-C": ["Superpowered Street Gangs", "Low-Magic Dungeon Crawler"],
        "9-B": ["Military PsyOps City", "Modern Sorcery Academy"],
        "0": ["The Meta Abyss", "Chrono-collapse Realm"]
    }
    name = random.choice(inspirations.get(tier, ["Unknown World"]))

    return {
        "name": name,
        "tone": random.choice(["mysterious", "heroic", "tragic", "comedic"]),
        "summary": f"You are transmigrated into {name}, a place of {tier} tier danger and destiny.",
        "tier": tier,
        "canon_profile": {
            "name": "Default Protagonist",
            "background": "A known figure from this world with embedded ties and secrets."
        },
        "inspiration": name
    }