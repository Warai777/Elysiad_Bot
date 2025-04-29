import random

class ChoiceEngine:
    def __init__(self):
        self.choices = []
        self.death_choice = None
        self.progress_choice = None
        self.lore_choices = []
        self.random_choice = None

    def generate_choices(self):
        base_actions = [
            "Enter the glowing portal.",
            "Climb the blackened tower.",
            "Follow the whispering voice.",
            "Touch the floating crystal.",
            "Wait silently in the shadows."
        ]
        random.shuffle(base_actions)  # Shuffle so player can’t predict

        self.death_choice = random.randint(1, 5)
        available = [i for i in range(1, 6) if i != self.death_choice]
        self.progress_choice = random.choice(available)
        available.remove(self.progress_choice)

        self.lore_choices = random.sample(available, 2)
        available = [i for i in available if i not in self.lore_choices]

        self.random_choice = available[0]

        # Create final choices mapping
        self.choices = [(i+1, action) for i, action in enumerate(base_actions)]

    def resolve_choice(self, selected_choice):
        if selected_choice == self.death_choice:
            return "death"
        elif selected_choice == self.progress_choice:
            return "progress"
        elif selected_choice in self.lore_choices:
            return "lore"
        elif selected_choice == self.random_choice:
            # 50% chance good or bad
            roll = random.randint(1, 100)
            return "good" if roll >= 50 else "bad"
        else:
            return "invalid"
