import json
import random
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_inspired_companion(world_inspiration):
    prompt = f"""
You are generating a fictional RPG companion inspired by the world of {world_inspiration}.
Your job is to:
- Pick a well-known character archetype from that world
- Rename and redesign them to avoid copyright
- Keep them recognizable to fans
- Assign them VS Battle Wiki-style stats and abilities

Respond strictly in JSON format:
{{
  "name": "RenamedCharacter",
  "inspired_by": "Original Character",
  "archetype": "Reworded role (e.g., Spirit Exorcist Captain)",
  "tier": "(e.g., 7-A, Low 6-B, High 1-C)",
  "stats": {{
    "attack": "City-level punches with shockwaves",
    "speed": "Hypersonic reactions",
    "durability": "Tank shell resistance",
    "range": "Mid-range energy blasts (hundreds of meters)",
    "intelligence": "Strategic battle genius",
    "stamina": "Can fight for days without rest"
  }},
  "ability": {{
    "name": "Renamed Technique",
    "description": "A reworded signature move inspired by the original."
  }},
  "personality": "1-sentence summary of their personality",
  "loyalty": {random.randint(50, 90)}
}}
"""

   try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a character generator for an RPG project."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=600
    )

    content = response.choices[0].message.content
    companion_data = json.loads(content)

    # ✅ Validate essential keys
    required_keys = ["name", "tier", "stats", "ability", "personality", "loyalty"]
    if not all(k in companion_data for k in required_keys):
        raise ValueError("❌ Incomplete AI companion data.")

    # ✅ Validate nested keys in stats and ability
    stat_keys = ["attack", "speed", "durability", "range", "intelligence", "stamina"]
    if not all(k in companion_data["stats"] for k in stat_keys):
        raise ValueError("❌ Missing stat fields in AI companion data.")

    if "name" not in companion_data["ability"] or "description" not in companion_data["ability"]:
        raise ValueError("❌ Incomplete ability fields.")

    return companion_data


    except Exception as e:
        print("⚠️ Companion generation failed:", e)
        return {
            "name": "Fallback Echo",
            "inspired_by": world_inspiration,
            "archetype": "Shadowed Wanderer",
            "tier": "Unknown",
            "stats": {
                "attack": "Unknown",
                "speed": "Unknown",
                "durability": "Unknown",
                "range": "Unknown",
                "intelligence": "Unknown",
                "stamina": "Unknown"
            },
            "ability": {
                "name": "Memory Spark",
                "description": "A faint echo of a forgotten warrior's power."
            },
            "personality": "Mysterious and calm, with flickers of purpose.",
            "loyalty": random.randint(40, 60)
        }
