import os
from openai import OpenAI

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
You are an AI storyteller within a darkly immersive light novel engine. You are about to generate a completely original story scene for a player who has transmigrated into a new world. This world is procedurally generated, but its tone and atmosphere are inspired by a popular fictional work. You must avoid referencing any copyrighted names, characters, or settings directly, but you can mimic the tone, themes, world structure, and feel in a transformative, original way.

Context:
- The player is in a world called: "{world_name}"
- The tone of this world is: "{tone}" (examples: mystical, grimdark, heroic, psychological, cosmic, etc.)
- The world was inspired by: "{inspiration}"
- The player has these personality traits: {trait_description}
- These companions are with the player: {companion_summary}
- Their journal contains these vague hints: {hint_summary}
- Phase of story: "{phase}" (Intro, Exploration, Tension, Climax, Resolution, Failure)

Instructions:
1. Write in the second person ("you") and style the scene like a light novel.
2. Make the world feel living, strange, and emotionally immersive.
3. Describe at least one meaningful thing the player sees or experiences that will return later in the story.
4. Include at least one specific moment where the environment or a character reacts to the player in a subtle way.
5. Never mention the real source material directly (e.g., Bleach, Marvel), but match the feel.
6. Do not include game mechanics or rules.
7. After writing the immersive scene, output exactly five story choices. Format them as a JSON list like this:
["Choice A", "Choice B", "Choice C", "Choice D", "Choice E"]
Each option should feel like a valid action in the story, but hide whether it leads to death, world-building, progress, or randomness.

Return a JSON object with two keys:
- "story": the full generated story segment
- "choices": the list of five story options

Begin the response now in proper JSON format.
        """

        response = client.chat.completions.create(
            model=self.ai_model,
            messages=[
                {"role": "system", "content": "You are an immersive narrative engine for a light novel-style game."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=1200,
        )

        result = response.choices[0].message.content
        return result
