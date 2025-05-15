# roll_engine.py
import random

def roll_action(modifiers=0):
    base_roll = random.randint(1, 100)
    final_roll = min(100, max(1, base_roll + modifiers))
    return final_roll

def interpret_roll(roll):
    if roll <= 49:
        return 'negative'
    elif 50 <= roll <= 89:
        return 'positive'
    else:
        return 'critical_success'