import random

def roll_success():
    return random.randint(1, 100)

def evaluate_choice(input_text, character_traits, canon_profile):
    roll = roll_success()
    score = 0

    if any(trait in input_text.lower() for trait in character_traits):
        score += 20

    if input_text.lower() in canon_profile.get("valid_actions", []):
        score += 40
    elif input_text.lower() in canon_profile.get("forbidden_actions", []):
        score -= 60

    result_score = roll + score
    if result_score >= 75:
        return "positive", result_score
    elif result_score >= 45:
        return "neutral", result_score
    else:
        return "negative", result_score