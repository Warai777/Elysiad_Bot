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


def generate_story_segment(world, companions, tone, player_traits, player_memory, phase="Intro"):
    world_name = world.get("name", "Unknown Realm")
    inspiration = world.get("inspiration", "an unfamiliar myth")
    tone = tone.lower()
    companion_names = [c["name"] for c in companions]
    companion_detail = random.choice(companion_names) if companion_names else "a shadow that follows"
    trait_description = " and ".join(player_traits)

    journal_hint = None
    if player_memory.get("Journal", {}).get("Hints"):
        journal_hint = random.choice(player_memory["Journal"]["Hints"])
    else:
        journal_hint = "The Archivist’s journal remains frustratingly vague."

    base_intro = {
        "grimdark": f"{world_name} is soaked in rust and regret. The ground crunches with old bones and broken crowns.",
        "surreal": f"Colors drip from the sky like paint. In {world_name}, logic is a myth, and the wind speaks in riddles.",
        "mystical": f"{world_name} breathes with arcane pulse. Trees glow faintly. Rivers hum forgotten songs.",
        "heroic": f"The banners of lost kingdoms ripple above {world_name}. You feel destiny crawling up your spine.",
        "melancholy": f"{world_name} rests in mourning. Every stone bears the weight of untold sorrow.",
        "cosmic": f"{world_name} tilts beneath stars that shouldn’t exist. Something ancient stirs beyond the veil.",
        "spiritual": f"In {world_name}, spirits whisper from the roots. Your every step echoes through unseen realms.",
        "dreamlike": f"{world_name} bends like a memory half-remembered. You feel lighter than thought itself.",
        "psychological": f"You’re not sure you’re alone in your mind. {world_name} blurs the line between thought and place.",
        "adventurous": f"The winds of {world_name} beckon like a challenge. Hidden temples and leviathans lie ahead."
    }

    intro = base_intro.get(tone, base_intro["mystical"])

    phase_block = {
        "Intro": f"""
You arrive in {world_name}, your {trait_description} nature on edge. The air hums — not with sound, but with tension. 
Alongside you, {companion_detail} says nothing, but watches everything.

{journal_hint}
""",

        "Exploration": f"""
You trek deeper into {world_name}, paths winding and strange. Your senses sharpen — every shift in wind, every flicker of light draws your eye. 
{companion_detail} moves quietly beside you, scanning the strange terrain for danger or wonder.

The Archivist’s hint resurfaces in your thoughts. Meaning still eludes you.
""",

        "Tension": f"""
A shriek in the distance cuts the silence. You and {companion_detail} freeze, hearts racing. The ground trembles as if reacting.

Your instincts scream, but there's no clear threat — only the pressure of being watched.
""",

        "Climax": f"""
You find yourself at a crossroads beneath a sky of fractured moons. The journal hint blazes in your mind — it was always leading here.
{companion_detail} draws their weapon, and your next step may change everything.
""",

        "Resolution": f"""
The world breathes again. Whatever trial you faced now lingers like smoke in the wind. 
{companion_detail} rests their back against a broken monument, silent.

You survived. For now.
""",

        "Failure": f"""
You collapse, the world dimming around you. In the shadows, {companion_detail} kneels — silent, grieving. 

The journal page turns blank. Your story in {world_name} has paused — not ended.
"""
    }

    return f"{intro}\n\n{phase_block.get(phase, phase_block['Exploration'])}\n\nThis place, born from the echoes of **{inspiration}**, watches you in return..."
