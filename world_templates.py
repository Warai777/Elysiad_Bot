import openai
import json

def generate_ai_world_template():
    prompt = """
Create a fictional world template for a light novel-style RPG.

RULES:
- The world must have a ONE-WORD NAME that is poetic, symbolic, and clearly inspired by a well-known fictional universe (e.g., One Piece, Bleach, Dragon Ball, Lord of the Mysteries, etc.)
- DO NOT include any copyrighted terms.
- It must be recognizable to fans as being inspired by that universe.
- Match the tone and themes of that world.

Return the following JSON object:
{
  "name": "OneWordNameHere",
  "tone": "1-2 word mood descriptor (e.g. grimdark, mystical)",
  "inspiration": "The fictional work it's based on (e.g., Bleach, One Piece)",
  "summary": "1-2 sentence poetic summary describing the world."
}
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
        print("⚠️ AI world generation failed:", e)
        return {
            "name": "Nullspire",
            "tone": "mystical",
            "inspiration": "Original",
            "summary": "A shrouded land adrift between time and ruin."
        }
