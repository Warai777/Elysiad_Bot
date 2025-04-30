import random

def generate_story_segment(world, companions, tone, player_traits, phase="Exploration"):
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

    phase_flavor = {
        "Exploration": f"You wander through the {world_name}, your {trait_description} nature alert to every shift in the air.",
        "Tension": f"A noise cracks the silence. Somewhere unseen, something watches. Your breath catches in your throat.",
        "Climax": f"You're out of options. This moment — whatever it is — has been building for some time. And now, it's here.",
        "Resolution": f"Whatever trial you've faced, the echo of it lingers. The dust hasn't settled, but you’re still standing.",
        "Failure": f"You faltered — the world didn't wait. Now, even your shadow seems to judge you.",
    }

    intro = base_descriptions.get(tone, base_descriptions["mystical"])
    middle = phase_flavor.get(phase, phase_flavor["Exploration"])
    outro = f"Alongside you, {companion_detail} keeps close. The Archivist’s hint flickers in your journal, unreadable but heavy with meaning."

    return f"{intro}\n\n{middle}\n\n{outro}"
