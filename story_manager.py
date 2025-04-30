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


def generate_story_segment(world, companions, tone, player_traits, player_memory, phase="Exploration"):
    world_name = world.get("name", "Unknown Realm")
    inspiration = world.get("inspiration", "an unfamiliar myth")
    tone = tone.lower()
    companion_names = [c["name"] for c in companions]
    companion_detail = random.choice(companion_names) if companion_names else "a shadow that follows"
    trait_description = " and ".join(player_traits)

    # Memory-based callback (previous hint or event)
    hints = player_memory.get("Journal", {}).get("Hints", [])
    recent_hint = random.choice(hints) if hints else "The Archivist’s journal remains frustratingly vague."

    events = player_memory.get("Journal", {}).get("Events", [])
    recalled_event = random.choice(events) if events else None

    # Tone-based world introduction
    tone_descriptions = {
        "grimdark": f"The sky above {world_name} bleeds rust. Hope here is a rumor, whispered and long dead.",
        "surreal": f"In {world_name}, buildings bend, clocks hum, and thoughts sometimes drip from your ears. Nothing is stable.",
        "mystical": f"{world_name} breathes like a sleeping god. Even the stones carry whispers of forgotten chants.",
        "heroic": f"The banners of {world_name} ripple in unseen wind. Somewhere, fate sharpens its blade for you.",
        "melancholy": f"Everything in {world_name} feels like the last echo of a goodbye — delicate, irreversible.",
        "cosmic": f"Above {world_name}, the stars blink in impossible languages. You feel watched, weighed, and maybe rewritten.",
        "spiritual": f"The trees hum. The rivers speak. {world_name} is alive in a way no world should be.",
        "dreamlike": f"You’re walking through someone else’s dream. Every breath in {world_name} tastes like memory.",
        "psychological": f"{world_name} turns inward — you hear your own voice echo from other mouths.",
        "adventurous": f"Mountains claw the horizon. Towns bustle beneath floating isles. {world_name} begs to be charted."
    }
    intro = tone_descriptions.get(tone, tone_descriptions["mystical"])

    # Phase-based flavor
    phase_flavor = {
        "Intro": f"You blink against strange light, your {trait_description} instincts struggling to parse this reality. Beside you, {companion_detail} adjusts slowly — both of you strangers in this place.",
        "Exploration": f"You venture deeper, your {trait_description} nature tuned to the oddities around you. The wind smells of salt and metal. {companion_detail} says nothing, but watches everything.",
        "Tension": f"A chill lances the silence. Your breath draws slower. {companion_detail} places a hand on something hidden. You sense you're not alone.",
        "Climax": f"You've come too far to stop now. The air thickens. Every step feels like a choice between victory or consequence.",
        "Resolution": f"The echoes fade. The world feels quieter, though nothing here is ever truly safe. {companion_detail} lets out a sigh they didn’t know they were holding.",
        "Failure": f"Your body moves, but you don’t feel it. The world pressed harder than expected. You are still breathing, but that’s all."
    }
    phase_block = phase_flavor.get(phase, phase_flavor["Exploration"])

    # Callback text
    callback = f"A faint memory resurfaces: \"{recalled_event}\"" if recalled_event else ""
    hint_text = f"The Archivist’s last hint echoes: “{recent_hint}”"

    # Final composition
    return f"""{intro}

{phase_block}

{callback}
{hint_text}

This place, born from the echoes of **{inspiration}**, watches you in return..."""
