import random

def generate_starting_scenario(world):
    tone = world.get("tone", "mystical")
    inspiration = world.get("inspiration", "Unknown World")
    name = world.get("name", "Unnamed Realm")

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

    arrival_variants = [
        f"You awaken inside the {name}.",
        f"The portal yawns open — and you're hurled into the {name}.",
        f"You stumble from the rift. Around you: {name}.",
        f"Your vision returns slowly. The first thing you see is the skyline of the {name}.",
    ]

    intro = random.choice(arrival_variants)
    flavor = base_feeling.get(tone, base_feeling["mystical"])

    return f"""{intro}

{flavor}

This is a world born from the echoes of **{inspiration}**.
You're not meant to be here — and yet, something deeper is beginning to stir...""".strip()
