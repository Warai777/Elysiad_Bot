import os
import json
import re
import openai

# ✅ Instantiate OpenAI v1.0+ client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class StoryManager:
    def __init__(self, ai_model="gpt-4"):
        self.ai_model = ai_model

    def generate_story_segment(self, world, companions, tone, player_traits, player_memory, phase="Intro"):
        world_name = world.get("name", "Unknown Realm")
        inspiration = world.get("inspiration", "an unfamiliar myth")
        tone = tone.lower()
        companion_names = [c["name"] for c in companions]
        companion_summary = ", ".join(companion_names) if companion_names else "no one but your own shadow"
        trait_description = ", ".join(player_traits)
        journal_hints = player_memory.get("Journal", {}).get("Hints", [])
        if not journal_hints:
            journal_hints = ["The Archivist’s journal remains frustratingly vague."]
        hint_summary = "; ".join(journal_hints)

        prompt = f"""
You are an AI storyteller within a darkly immersive light novel engine. Generate a completely original story scene in strict JSON format.

Context:
- World: "{world_name}"
- Tone: "{tone}"
- Inspiration: "{inspiration}"
- Traits: {trait_description}
- Companions: {companion_summary}
- Journal Hints: {hint_summary}
- Phase: "{phase}"

Instructions:
1. Write in second person ("you").
2. Style the scene like a light novel.
3. Make the world vivid, alive, and emotionally immersive.
4. Describe one meaningful element that returns later.
5. Include one subtle reaction from the environment or a character.
6. Do NOT mention real-world IP or game mechanics.
7. Return ONLY valid JSON (no preamble, no markdown, no prose).

Respond strictly with:
{{
  "story": "Immersive story scene here...",
  "choices": ["Choice A", "Choice B", "Choice C", "Choice D", "Choice E"]
}}
        """

        try:
            response = client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are an immersive narrative engine for a light novel-style game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.95,
                max_tokens=1200,
            )

            raw_content = response.choices[0].message.content

            # Sanitize output
            cleaned_content = re.sub(r'[\x00-\x1F\x7F]', '', raw_content)
            parsed = json.loads(cleaned_content)

            if "story" not in parsed or "choices" not in parsed:
                raise ValueError("Missing 'story' or 'choices' key in AI response.")

            return parsed["story"], parsed["choices"]

        except json.JSONDecodeError as e:
            print("❌ JSON decoding failed:", e)
            print("⚠️ Raw response (truncated):", repr(raw_content[:500]))
            raise

        except Exception as e:
            print("❌ Unexpected error while parsing story segment:", e)
            raise
