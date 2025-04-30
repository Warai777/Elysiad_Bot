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
    trait_description = " and ".join(player_traits)

    # Choose a companion (or fallback)
    companion_names = [c["name"] for c in companions]
    companion_detail = random.choice(companion_names) if companion_names else "a shadow that follows"

    # Tone intro descriptions
    base_descriptions = {
        "grimdark": f"The sky over {world_name} bleeds rust and ash. Every breath feels borrowed. Blood crusts the stones like history that won't be washed away. Buildings crumble like broken promises, and somewhere, something is watching.",
        "surreal": f"In {world_name}, reality doesn't hold. The trees sway out of sync with the wind. Colors blur, words echo before they're spoken. A floating staircase spirals toward a sky that flickers like an old film.",
        "mystical": f"The world of {world_name} hums with forgotten wisdom. Ruins breathe. Rivers sing. Crystals blink open like eyes. As you walk, the wind speaks your name in a voice older than time.",
        "heroic": f"{world_name} stands proud. Flags whip in high winds. You hear chants on the wind, see armor gleam on distant cliffs. Destiny isn’t whispered here — it roars.",
        "melancholy": f"Everything beautiful in {world_name} feels faded. A song without a singer, a kingdom without a crown. Even the sunlight feels like a goodbye.",
        "cosmic": f"The constellations in {world_name} move. Not slowly, but like they know you're watching. Gravity changes with your thoughts. Time pools in corners.",
        "spiritual": f"Every path in {world_name} feels chosen. You pass shrines without prayers, bones woven into trees, and faces in the water that watch without blinking.",
        "dreamlike": f"{world_name} bends softly around you, like a memory reshaping itself. The grass glows. Footsteps echo in places you haven’t yet stepped.",
        "psychological": f"In {world_name}, your thoughts no longer feel like your own. Reflections linger too long. You see flashes of other versions of yourself — bleeding, laughing, watching.",
        "adventurous": f"The jungle breathes heat. Laughter drifts on the breeze. Ruins beckon, traps hum with anticipation, and somewhere, treasure sings."
    }

    phase_flavor = {
        "Intro": f"You find yourself standing still. A presence looms — not in the shadows, but within you. It’s your own fear, your own hope. The first step isn’t on the path — it’s through your own soul.",
        "Exploration": f"You wander through {world_name}, your {trait_description} nature alert to every shift in the air. Behind you, the world seals the entrance — there's no going back.",
        "Tension": f"A sound breaks the stillness — not loud, but wrong. The silence that follows feels heavier than noise.",
        "Climax": f"The path ends. You’ve run long enough. Here, the world demands something — and it won’t wait for your permission.",
        "Resolution": f"You’ve seen it now. What lies behind the veil. The wind moves differently. You are no longer who you were.",
        "Failure": f"The world has judged you. Whether fairly or not, it has moved on. You are alone in its wake."
    }

    # Build the complete immersive intro
    intro = base_descriptions.get(tone, base_descriptions["mystical"])
    phase_text = phase_flavor.get(phase, phase_flavor["Exploration"])
    outro = f"\n\nAlongside you, {companion_detail} walks in silence. The Archivist’s hint flickers again in your journal — still unreadable, but pulsing with meaning. The world of **{world_name}**, born from the echoes of *{inspiration}*, stretches endlessly before you."

    return f"{intro}\n\n{phase_text}\n{outro}"
