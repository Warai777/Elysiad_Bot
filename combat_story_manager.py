import random

class CombatStoryManager:
    def __init__(self, player, companions, world_tone):
        self.player = player
        self.companions = companions
        self.world_tone = world_tone

    def generate_combat_result(self, action_choice, success=True):
        tone = self.world_tone.lower()

        base_stories = {
            "charge": [
                "You rush forward without hesitation, fists colliding with brutal force.",
                "Your charge smashes into your foe like a thunderclap!",
                "Raw momentum carries you through, battering defenses aside."
            ],
            "environment": [
                "You tear a loose stone from the ground and hurl it!",
                "A hanging beam breaks loose under your kick, crashing down onto the enemy.",
                "You duck behind debris, twisting the battlefield to your favor."
            ],
            "stall": [
                "You feint left, dodge right, always a step ahead.",
                "You buy seconds, precious and desperate, evading each blow narrowly.",
                "Breath ragged, you weave through the chaos, stalling the inevitable."
            ],
            "outwit": [
                "A smirk crosses your lips — they fall for the bait.",
                "You feign weakness, striking the moment their guard drops.",
                "You plant doubt with a whisper, and hesitation seals their fate."
            ],
            "brace": [
                "You ground your stance, absorbing the coming shock.",
                "The world narrows to the strike — and you endure it.",
                "Every muscle tenses; you survive, battered but unbroken."
            ]
        }

        tone_modifiers = {
            "mysterious": "The shadows seem to aid or hinder without warning.",
            "grimdark": "Blood sprays like ink across the broken ground.",
            "heroic": "Every breath sings of stubborn defiance.",
            "surreal": "Reality bends: color smears, sound warps around you.",
            "psychological": "Your mind splinters between fear and clarity.",
            "cosmic": "For a moment, you glimpse impossible patterns in the air.",
            "melancholy": "Even victory tastes of ash and forgotten dreams."
        }

        scars = [
            "A deep gash burns along your side.",
            "A rib cracks under the force of a stray blow.",
            "Pain lingers in your arm — a reminder of your mortality."
        ]

        instincts = [
            "Your instincts sharpen: next time, you will strike faster.",
            "You sense threats before they move — a whisper of foresight.",
            "Fear tempers into steel in your veins."
        ]

        # --- Pick a random story depending on the action
        action_keys = ["charge", "environment", "stall", "outwit", "brace"]
        if action_choice < 0 or action_choice >= len(action_keys):
            action_choice = 0  # fallback safety
        action_type = action_keys[action_choice]
        base_story = random.choice(base_stories[action_type])

        # --- Tone flavor
        tone_text = tone_modifiers.get(tone, "")

        # --- Outcome
        if success:
            instinct_gain = random.random() < 0.5  # 50% chance to gain instinct
            scar = False
        else:
            instinct_gain = False
            scar = random.random() < 0.7  # 70% chance you take a scar

        # --- Build Final Narrative
        narrative = f"{base_story} {tone_text}"

        scar_text = random.choice(scars) if scar else None
        instinct_text = random.choice(instincts) if instinct_gain else None

        return narrative, scar_text, instinct_text
