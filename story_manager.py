# story_manager.py
# Handles global story phase transitions and world-specific narrative logic

def generate_story_scene(session):
    phase = session.current_phase
    world = session.current_world or "generic"

    if world == "One Piece":
        return handle_one_piece_phase(session, phase)
    elif world == "Death Note":
        return handle_death_note_phase(session, phase)
    else:
        return handle_generic_phase(session, phase)

def handle_generic_phase(session, phase):
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
        return "Your journey pauses in quiet reflection."

def handle_one_piece_phase(session, phase):
    if phase == "Intro":
        session.advance_phase("Training")
        return "You begin your life as a young pirate dreamer in East Blue."
    elif phase == "Training":
        session.advance_phase("Recruiting")
        return "You seek crewmates and test your blade against bandits."
    elif phase == "Recruiting":
        session.advance_phase("Grand Line")
        return "The sea opens to legend and danger."
    elif phase == "Grand Line":
        session.advance_phase("New World")
        return "You must now face the emperors of the sea."
    else:
        return "Quiet tides wash over the Thousand Sunny..."

def handle_death_note_phase(session, phase):
    if phase == "Intro":
        session.advance_phase("Discovery")
        return "You find a black notebook lying in the street..."
    elif phase == "Discovery":
        session.advance_phase("Conflict")
        return "Others begin to notice your patterns..."
    elif phase == "Conflict":
        session.advance_phase("Collapse")
        return "Suspicions tighten. Your world shrinks."
    elif phase == "Collapse":
        session.advance_phase("Judgment")
        return "Only one will outsmart the other."
    else:
        return "The pages fall silent for now..."