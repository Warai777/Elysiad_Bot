import random
import json

TIER_POOL = ["10-C", "10-B", "10-A", "9-C", "0"]

def generate_ai_world_template():
    # Placeholder static data for now
    name = random.choice(["Aeonfall", "Thorneveil", "Yureisen", "Frosthollow"])
    tone = random.choice(["melancholic", "bright", "oppressive", "mysterious"])
    inspiration = random.choice(["anime", "book", "webtoon", "game"])
    tier = "10-C"  # default for now

    summary = f"In the land of {name}, where {tone} forces rule and destiny sleeps beneath cracked stone..."
    canon_profile = {
        "name": random.choice(["Kael", "Rin", "Asher", "Luna"]),
        "arc": "Rebirth of the Flame",
        "intro_paragraph": f"You awaken as the heir to a ruined family in the land of {name}, shrouded in silence and schemes."
    }

    return {
        "name": name,
        "tone": tone,
        "inspiration": inspiration,
        "summary": summary,
        "tier": tier,
        "canon_profile": canon_profile
    }