import openai
import os

# ✅ OpenAI v1.0+ client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GenreManager:
    def __init__(self):
        self.available_genres = [
            "Happy",
            "Mysterious",
            "Grimdark",
            "Surreal",
            "Epic",
            "Fantasy",
            "Sci-Fi",
            "Horror",
            "Tragic Poetic",
            "Dark Heroism"
        ]

    def get_genre_style(self, genre):
        styles = {
            "Happy": "bright, hopeful, colorful imagery",
            "Mysterious": "foggy, cautious, secretive atmosphere",
            "Grimdark": "bleak, brutal, despairing tone",
            "Surreal": "dreamlike, absurd, reality-warped style",
            "Epic": "grand, sweeping, legendary scale",
            "Fantasy": "magical, classic mythic worlds",
            "Sci-Fi": "cold, high-tech, futuristic or dystopian tone",
            "Horror": "fear-driven, visceral dread, darkness everywhere",
            "Tragic Poetic": "beautiful sadness, memory and loss",
            "Dark Heroism": "grim determination, noble suffering"
        }
        return styles.get(genre, "mysterious and unknown")

    def expand_genre_with_ai(self, genre):
        prompt = f"""
You are a tone stylist. Take the genre "{genre}" and expand it into:
- A rich narrative description (1-2 sentences)
- A poetic tone summary
- A theme suggestion for how it affects the world

Respond strictly in JSON:
{{
  "description": "...",
  "tone": "...",
  "world_effect": "..."
}}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a literary tone expansion engine."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )

            return response.choices[0].message.content

        except Exception as e:
            print("⚠️ AI genre expansion failed:", e)
            return None
