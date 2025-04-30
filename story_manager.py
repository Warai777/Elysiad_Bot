import openai

class StoryManager:
    def __init__(self, ai_model):
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
- The world was inspired by: "{inspiration}" (this is a theme or work like "Bleach", "Reverend Insanity", "God of War", etc.)
- The player has these personality traits: {trait_description}
- These companions are with the player: {companion_summary}
- Their journal contains these vague hints: {hint_summary}
- Phase of story: "{phase}" (Intro, Exploration, Tension, Climax, Resolution, Failure)

Instructions:
- Write in the second person ("you") and style the scene like a light novel.
- Make the world feel living, strange, and emotionally immersive.
- Describe at least one meaningful thing the player sees or experiences that will return later in the story.
- Include at least one specific moment where the environment or a character reacts to the player in a subtle way.
- Never mention the real source material directly (e.g., Bleach, Marvel), but match the feel.
- Do not write choices or game instructions. Just return the story scene text itself.

Begin the story segment now.
        """

        response = openai.ChatCompletion.create(
            model=self.ai_model,
            messages=[
                {"role": "system", "content": "You are an immersive narrative engine for a light novel-style game."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=1000
        )

        return response['choices'][0]['message']['content'].strip()
