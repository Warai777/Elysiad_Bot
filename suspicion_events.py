# suspicion_events.py

def check_suspicion_thresholds(session):
    if session.suspicion >= 100:
        return "World rejects you. Narrative collapse imminent."
    elif session.suspicion >= 70:
        return "Whispers follow your steps. NPCs grow wary."
    elif session.suspicion >= 40:
        return "Minor anomalies ripple through the shard."
    return None