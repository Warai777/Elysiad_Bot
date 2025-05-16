import random

def generate_story_scene(session):
    phase = session.current_phase
    if phase == "Intro":
        session.advance_phase("Exploration")
        return "You awaken in a mysterious world. Your journey begins."
    elif phase == "Exploration":
        session.advance_phase("Tension")
        return "You uncover ancient ruins hinting at deeper secrets."
    elif phase == "Tension":
        session.advance_phase("Climax")
        return "A confrontation brews. Allies waver. Foes rally."
    elif phase == "Climax":
        session.advance_phase("Resolution")
        return "With everything at stake, you make your final move."
    else:
        return "Your journey has reached a moment of calm. The tale pauses..."