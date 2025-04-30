import re

class StoryManager:
    def __init__(self, ai_model):
        self.ai_model = ai_model

    def generate_story_segment(self, player, world, companions, phase):
        world_name = world.get("name", "Unknown World")
        inspiration = world.get("inspiration", "an unknown tale")
        tone = world.get("tone", "mystical")
        traits = ", ".join(player.traits)
        companion_names = [c["name"] for c in companions]
        companion_line = f"{random.choice(companion_names)} walks beside you." if companion_names else "You move alone."

        journal = player.memory.get("Journal", {})
        hints = journal.get("Hints", [])
        journal_hint = random.choice(hints) if hints else "The Archivist left you no clue this time."

        narrative_threads = player.memory.setdefault("NarrativeThreads", [])
        callbacks = "\n".join(f"- {thread}" for thread in narrative_threads[-3:])  # Limit to last 3 for context

        prompt = f"""
You are writing a second-person immersive scene like a light novel. The player is in {world_name}, a realm inspired by {inspiration}.
The tone is {tone}, and the story is currently in the "{phase}" phase.

Traits: {traits}
Companion: {companion_line}
Archivist Hint: {journal_hint}
Callback Threads: {callbacks or "None yet."}

Write a vivid, emotional, highly detailed scene where the environment, past memories, or subtle world rules might matter later.
Include sensory language, pacing, internal thought, and physical reactions.
DO NOT summarize — immerse the player completely in this moment.
        """.strip()

        output = self.ai_model.generate(prompt)

        # Parse and extract a key moment for future reference
        new_thread = self.extract_significant_moment(output)
        if new_thread:
            narrative_threads.append(new_thread)
            player.memory["NarrativeThreads"] = narrative_threads
            player.save()

        return output

    def extract_significant_moment(self, scene_text):
        """
        Extract a possible narrative thread for reuse based on key phrases.
        """
        # Look for lines involving something "unusual", "noted", or "strange"
        patterns = [
            r'You notice (something|someone|a figure|an object|an anomaly)[^\.]+[\.]',
            r'(Strangely|Oddly),[^\.]+[\.]',
            r'There is (a|an) (faint|strange|glimmering|unusual)[^\.]+[\.]',
            r'In the distance,[^\.]+[\.]',
            r'Something feels off[^\.]*[\.]'
        ]

        for pattern in patterns:
            match = re.search(pattern, scene_text, re.IGNORECASE)
            if match:
                return match.group().strip()

        # Fallback: extract the first vivid sensory sentence
        lines = scene_text.splitlines()
        for line in lines:
            if len(line.split()) >= 6 and any(word in line.lower() for word in ["hear", "feel", "see", "notice", "watch", "tremble"]):
                return line.strip()

        return None
