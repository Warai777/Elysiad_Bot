import random

INSPIRATION_TAGS = {
    "Twilight Cradle": "Made in Abyss",
    "City of Hollow Dreams": "Persona + Inception",
    "Vault of Shattered Stars": "Mass Effect + Gurren Lagann",
    "Sea of Endless Horizons": "One Piece",
    "Forest of Distant Echoes": "Princess Mononoke",
    "Labyrinth of Forgotten Sins": "Dark Souls + Berserk",
    "Crown of Falling Leaves": "Ori + Bleach",
}

TONE_TAGS = {
    "Twilight Cradle": "mystical",
    "City of Hollow Dreams": "psychological",
    "Vault of Shattered Stars": "cosmic",
    "Sea of Endless Horizons": "adventurous",
    "Forest of Distant Echoes": "spiritual",
    "Labyrinth of Forgotten Sins": "grimdark",
    "Crown of Falling Leaves": "melancholy"
}

def generate_world():
    fragments_a = ["Vault", "Cradle", "Throne", "City", "Forest", "Ruins", "Mirror", "Wound", "Sea", "Crown"]
    fragments_b = ["of Shattered Stars", "of Endless Horizons", "of Distant Echoes", "of Forgotten Sins", "of Hollow Dreams", "of Falling Leaves", "of Lost Suns", "of Flickering Gods"]

    name = f"{random.choice(fragments_a)} {random.choice(fragments_b)}"
    inspiration = random.choice(list(INSPIRATION_TAGS.values()))
    tone = random.choice(["mystical", "grimdark", "surreal", "melancholy", "cosmic", "heroic", "dreamlike", "adventurous", "tragic", "romantic", "spiritual"])

    return {
        "name": name,
        "inspiration": inspiration,
        "tone": tone
    }
