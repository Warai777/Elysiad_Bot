import random
from genre_manager import GenreManager

genre_manager = GenreManager()

class StoryEngine:
    def __init__(self, genre):
        self.genre = genre

    def generate_story_intro(self, world_name):
        style = genre_manager.get_genre_style(self.genre)
        return f"""
In the realm of <b>{world_name}</b>, the air hums with <i>{style}</i>.
You feel the weight of countless choices ahead — each one alive with consequence.
Some paths may lead to ruin, others to revelation. But one thing is certain:
This is where your true story begins.
""".strip()

def generate_starting_scenario(world):
    tone = world.get("tone", "mystical")
    inspiration = world.get("inspiration", "Unknown World")
    name = world.get("name", "Unnamed Realm")

    arrival_variants = [
        f"You awaken inside the {name}.",
        f"The portal yawns open — and you're hurled into the {name}.",
        f"You stumble from the rift. Around you: {name}.",
        f"Your vision returns slowly. The first thing you see is the skyline of the {name}.",
    ]

    base_feeling = {
        "grimdark": "The air reeks of rust and sorrow. Nothing here remembers mercy.",
        "surreal": "Time hiccups as gravity stutters sideways — logic no longer binds the earth.",
        "adventurous": "The wind whips through salt-soaked sails. You crave the horizon.",
        "mystical": "Wisps of starlight drift like fog, humming with ancient secrets.",
        "heroic": "The banners rise. You were born to stand tall, even as storms howl.",
        "cosmic": "Space bends above your head — reality is thinning.",
        "melancholy": "Everything beautiful here is on the verge of breaking.",
        "dreamlike": "You can't remember how you arrived, but everything feels fragile — as if waking would break it.",
        "spiritual": "The trees whisper in a tongue you somehow understand. They're praying.",
        "psychological": "You aren't sure which thoughts are yours anymore.",
        "apocalyptic": "Ash falls like snow. Civilization has already lost.",
        "romantic": "Even the ruins blush when the sun kisses them.",
        "tragic": "Your boots echo in a place filled with echoes of loss.",
        "fantastical": "Dragons soar in the far distance. This world sings in color.",
        "suspenseful": "You are being watched. Every move weighs too much."
    }

    intro = random.choice(arrival_variants)
    feeling = base_feeling.get(tone, base_feeling["mystical"])

    return f"""{intro}

{feeling}

This is a world born from the echoes of <b>{inspiration}</b>.
You're not meant to be here — and yet, something deeper begins to stir...
""".strip()

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
        "Exploration": f"You wander through {world_name}, your {trait_description} nature alert to every shift in the air.",
        "Tension": f"A noise cracks the silence. Somewhere unseen, something watches. Your breath catches in your throat.",
        "Climax": f"You're out of options. This moment — whatever it is — has been building for some time. And now, it's here.",
        "Resolution": f"Whatever trial you've faced, the echo of it lingers. The dust hasn't settled, but you’re still standing.",
        "Failure": f"You faltered — the world didn't wait. Now, even your shadow seems to judge you.",
    }

    intro = base_descriptions.get(tone, base_descriptions["mystical"])
    middle = phase_flavor.get(phase, phase_flavor["Exploration"])
    outro = f"Alongside you, {companion_detail} keeps close. The Archivist’s hint flickers in your journal, unreadable but heavy with meaning."

    return f"{intro}\n\n{middle}\n\n{outro}"
