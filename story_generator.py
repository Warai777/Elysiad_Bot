import random

def generate_story_segment(world, companions, tone, player_traits):
    world_name = world.get("name", "Unknown Realm")
    inspiration = world.get("inspiration", "an unfamiliar myth")
    tone = tone.lower()
    companion_names = [c["name"] for c in companions]
    companion_detail = random.choice(companion_names) if companion_names else "a shadow that follows"
    trait_description = " and ".join(player_traits)

    base_descriptions = {
        "grimdark": f"The sky over {world_name} bleeds rust and ash. Every breath feels borrowed.",
        "surreal": f"The buildings breathe. Time bends sideways in the corners of your eyes.",
        "mystical": f"{world_name} hums with forgotten wisdom, its stones etched in starlight.",
        "heroic": f"You stand at the edge of destiny. The banners of {world_name} ripple with fate.",
        "melancholy": f"A silence settles over {world_name}, like a memory no one dares to recall.",
        "cosmic": f"The stars pulse overhead. In {world_name}, the void whispers truths you can't unhear.",
        "spiritual": f"The trees murmur prayers. Even the wind in {world_name} seems sentient.",
        "dreamlike": f"{world_name} flows like liquid memory. Each step feels like déjà vu.",
        "psychological": f"You doubt your own shadow. {world_name} has begun pulling at your identity.",
        "adventurous": f"Sunlight slices through canopies. {world_name} promises danger — and glory."
    }

    prompt = base_descriptions.get(tone, base_descriptions["mystical"])

    scene = f"""
{prompt}

You wander through {world_name}, your {trait_description} nature alert to every shift in the air.
Alongside you, {companion_detail} keeps close, gaze scanning the world as if expecting something.

There are no guides here. The Archivist’s words echo in your journal — cryptic, half-formed.
A fragment from your entry reads: *"The world resists those who don't belong."*

And yet, you walk forward — unbound by prophecy, unwritten by fate.
    """

    return scene.strip()
