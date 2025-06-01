# action_handler.py
from roll_engine import roll_action, interpret_roll

class ActionHandler:
    def __init__(self, session):
        self.session = session

    def handle_action(self, action_text, action_type):
        modifiers = 0
        if action_type == 'canon':
            modifiers += 15
        elif action_type == 'worldbuilding':
            modifiers += 5
        elif action_type == 'random':
            modifiers += 0
        elif action_type == 'death':
            modifiers -= 20
        elif action_type == 'suspicious':
            modifiers -= 10

        roll = roll_action(modifiers)
        outcome = interpret_roll(roll)

        result = {
            'action': action_text,
            'type': action_type,
            'roll': roll,
            'outcome': outcome
        }

        self.session.choice_log.append(result)

        # Suspicion handling
        suspicion_boost = 0
        if outcome == 'negative':
            suspicion_boost += 5
        if action_type == 'suspicious':
            suspicion_boost += 10

        if suspicion_boost > 0:
            self.session.suspicion += suspicion_boost
            self.session.companion_react("betrayal")

        # Reward logic
        if outcome == 'positive':
            self.session.origin_essence += 3
        elif outcome == 'critical_success':
            self.session.origin_essence += 10

        return result