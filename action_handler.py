# action_handler.py
from roll_engine import roll_action, interpret_roll

class ActionHandler:
    def __init__(self, session):
        self.session = session

    def handle_action(self, action_text, action_type):
        modifiers = 0
        if action_type == 'canon':
            modifiers += 15
        elif action_type == 'random':
            modifiers += 0
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

        # Adjust session stats based on outcome
        if outcome == 'negative':
            self.session.suspicion += 5
        elif outcome == 'positive':
            self.session.origin_essence += 3
        elif outcome == 'critical_success':
            self.session.origin_essence += 10

        return result