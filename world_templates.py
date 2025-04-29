import random

INSPIRATION_TAGS = [
    "One Piece", "Bleach", "Naruto", "Dragon Ball", "Attack on Titan",
    "Made in Abyss", "Fate Series", "Gurren Lagann", "Mass Effect",
    "Dark Souls", "Bloodborne", "Elden Ring", "Shadow Slave",
    "Lord of the Mysteries", "Reverend Insanity", "The Witcher",
    "Cyberpunk 2077", "Final Fantasy VII", "Persona Series", "Dorohedoro",
    "Vivy: Fluorite Eye's Song", "Steins;Gate", "Ergo Proxy",
    "Claymore", "Deadman Wonderland", "Overlord", "No Game No Life",
    "Death Note", "Tokyo Ghoul", "The Expanse", "Dune",
    "Star Wars", "Marvel Universe", "DC Universe",
    "Berserk", "Vinland Saga", "Fullmetal Alchemist", "Trigun",
    "The Mandalorian", "Arcane", "Eighty-Six (86)", "Zetman",
    "Cowboy Bebop", "Code Geass", "Hunter x Hunter", "Looney Tunes (Surreal Tone)",
    "God of War", "Halo", "Metro 2033", "Neon Genesis Evangelion",
    "Akira", "JoJo's Bizarre Adventure", "Black Clover"
]

TONE_POOL = [
    "mystical", "grimdark", "surreal", "melancholy", "cosmic",
    "heroic", "dreamlike", "adventurous", "tragic", "romantic",
    "spiritual", "psychological", "apocalyptic", "fantastical", "suspenseful"
]

NAME_FRAGMENTS_A = [
    "Vault", "Cradle", "Throne", "City", "Forest", "Ruins", "Mirror",
    "Wound", "Sea", "Crown", "Chasm", "Temple", "Citadel", "Abyss",
    "Furnace", "Obelisk", "Spires", "Hollow", "Labyrinth", "Veil"
]

NAME_FRAGMENTS_B = [
    "of Shattered Stars", "of Endless Horizons", "of Distant Echoes",
    "of Forgotten Sins", "of Hollow Dreams", "of Falling Leaves",
    "of Lost Suns", "of Flickering Gods", "of Withering Time",
    "of Silent Cries", "of Rusted Crowns", "of Broken Chains",
    "of Mourning Songs", "of Blighted Earth", "of Fading Embers",
    "of Eternal Bloom", "of Howling Voids", "of Crumbling Thrones",
    "of Sleeping Giants", "of Fractured Skies"
]

def generate_world():
    name = f"{random.choice(NAME_FRAGMENTS_A)} {random.choice(NAME_FRAGMENTS_B)}"
    inspiration = random.choice(INSPIRATION_TAGS)
    tone = random.choice(TONE_POOL)

    return {
        "name": name,
        "inspiration": inspiration,
        "tone": tone
    }
