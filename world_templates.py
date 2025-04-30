import openai
import json
import random
import os

# ✅ Set your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Large inspiration pool
FICTIONAL_INSPIRATIONS = [
    # Anime & Manga
    "One Piece", "Bleach", "Naruto", "Dragon Ball", "Attack on Titan", "Fullmetal Alchemist",
    "Jujutsu Kaisen", "Demon Slayer", "My Hero Academia", "Mob Psycho 100", "Chainsaw Man",
    "Tokyo Ghoul", "Hunter x Hunter", "Black Clover", "Fate/Stay Night", "Re:Zero",
    "Erased", "Death Note", "The Promised Neverland", "Vinland Saga", "Berserk", "Dororo",
    "Made in Abyss", "Parasyte", "Neon Genesis Evangelion", "Trigun", "Spy x Family",

    # Light/Web Novels
    "Lord of the Mysteries", "Shadow Slave", "Reverend Insanity", "Omniscient Reader’s Viewpoint",
    "Solo Leveling", "Trash of the Count’s Family", "The Beginning After the End",
    "I Shall Seal the Heavens", "Coiling Dragon", "The Legendary Mechanic",
    "Worlds’ Apocalypse Online", "He Who Fights With Monsters", "Dungeon Crawler Carl",
    "Mother of Learning", "Worm", "Super Minion", "The Wandering Inn",

    # Popular Movies
    "Star Wars", "The Matrix", "Inception", "The Lord of the Rings", "The Hobbit",
    "Interstellar", "Dune", "The Dark Knight", "Harry Potter", "John Wick", "Avatar",
    "The Hunger Games", "Mad Max", "Everything Everywhere All At Once",

    # TV Shows
    "Stranger Things", "Breaking Bad", "The Mandalorian", "The Witcher",
    "Game of Thrones", "The Boys", "Westworld", "Doctor Who", "Peaky Blinders",
    "Lost", "The Expanse", "Arcane", "The Last of Us",

    # Books & Western Fiction
    "The Name of the Wind", "Mistborn", "Stormlight Archive", "Red Rising", "Ender's Game",
    "The Wheel of Time", "Percy Jackson", "The Chronicles of Narnia", "His Dark Materials",
    "The First Law Trilogy", "The Dresden Files", "Discworld",

    # Video Games
    "Elden Ring", "Dark Souls", "Bloodborne", "Hollow Knight", "Final Fantasy",
    "Legend of Zelda", "The Witcher", "Skyrim", "Cyberpunk 2077", "Baldur's Gate",
    "League of Legends", "Hades", "Mass Effect", "Dragon Age", "Undertale",
    "Persona 5", "NieR Automata", "Genshin Impact", "Stellaris", "Dead Space",
    "Returnal", "Sekiro", "Minecraft", "Terraria"
]

def generate_ai_world_template():
    inspiration = random.choice(FICTIONAL_INSPIRATIONS)

    prompt = f"""
Create a fictional world template for a light novel-style RPG.

RULES:
- The world must have a ONE-WORD NAME that is poetic, symbolic, and clearly inspired by the fictional work "{inspiration}"
- DO NOT use copyrighted names or terms.
- It must be easily recognizable to fans of that universe.
- Match the tone and themes of the original work.

Return the following JSON object:
{{
  "name": "OneWordNameHere",
  "tone": "1-2 word mood descriptor (e.g. grimdark, mystical)",
  "inspiration": "{inspiration}",
  "summary": "1–2 sentence poetic summary describing the world."
}}

ONLY return valid JSON. Do not explain anything.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an RPG world generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=300
        )

        content = response.choices[0].message.content
        world = json.loads(content)
        return world

   except Exception as e:
    # Log the raw error to Render logs
    import sys
    print("⚠️ AI world generation failed:", file=sys.stderr)
    print(e, file=sys.stderr)
    return {
        "name": "Nullspire",
        "tone": "mystical",
        "inspiration": inspiration,
        "summary": "A shrouded land adrift between time and ruin."
    }

