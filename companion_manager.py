import json
import random
import openai
import os

# ✅ OpenAI v1.0+ client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_inspired_companion(world_inspiration):
    prompt = f"""
You are generating a fictional companion based on the world of {world_inspiration}.
Your goal is to:
- Select a well-known character from that world.
- Slightly rename and redesign them to avoid copyright.
- Keep them clearly recognizable by fans.
- Give them a unique ability (renamed and reworded).
- Describe their personality in 1 sentence.

Respond only in JSON like:
{{
  "name": "RenamedCharacter",
  "inspired_by": "Original Character",
  "archetype": "Reworded role (e.g., Soul Reaper Captain)",
  "ability": {{
    "name": "Echo Technique",
    "description": "A renamed ability based on the original."
  }},
  "personality": "Short description here."
}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a character generator for a procedurally generated RPG."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=400
        )

        content = response.choices[0].message.content
        companion_data = json.loads(content)
        companion_data["loyalty"] = random.randint(50, 90)
        return companion_data

    except Exception as e:
        print("⚠️ AI Companion generation failed:", e)

        return {
            "name": "Fallback Echo",
            "inspired_by": world_inspiration,
            "archetype": "Lost Wanderer",
            "ability": {
                "name": "Memory Spark",
                "description": "A faint echo of a forgotten warrior’s power."
            },
            "personality": "Mysterious and quiet, as if remembering another life.",
            "loyalty": random.randint(40, 60)
        }
