class NPCBehavior:
    def __init__(self, name, role="npc", loyalty=50):
        self.name = name
        self.role = role
        self.loyalty = loyalty  # 0–100 scale
        self.rivalry = 0  # Builds with hostile choices
        self.mood = "neutral"

    def update_relationship(self, action_tag):
        if action_tag == "betray":
            self.loyalty -= 25
            self.rivalry += 40
        elif action_tag == "assist":
            self.loyalty += 15
        elif action_tag == "ignore":
            self.loyalty -= 5

        self.loyalty = max(0, min(100, self.loyalty))
        self.rivalry = max(0, min(100, self.rivalry))

        if self.rivalry >= 70:
            self.mood = "vengeful"
        elif self.loyalty >= 80:
            self.mood = "devoted"
        else:
            self.mood = "neutral"

    def behavior_summary(self):
        return f"{self.name} [{self.role}] - Mood: {self.mood}, Loyalty: {self.loyalty}, Rivalry: {self.rivalry}"

    def react_to_suspicion(self, suspicion_level):
        if suspicion_level > 90:
            return f"{self.name} narrows their eyes. 'You're not who you say you are, are you?'"
        elif suspicion_level > 60:
            return f"{self.name} grows distant and cautious."
        elif suspicion_level > 30:
            return f"{self.name} starts asking odd questions about your past."
        return f"{self.name} seems at ease around you... for now."