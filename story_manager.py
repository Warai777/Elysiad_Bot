import os
from chapter_saver import save_chapter, load_chapter, advance_to_next_chapter

# story_manager.py
# Handles global story phase transitions and world-specific narrative logic

def generate_story_scene(session):
    phase = session.current_phase
    world = session.current_world or "generic"
    player_id = session.user_id or "default"
    chapter_num = session.current_chapter or 1
    entry_mode = session.entry_mode or "Canon"
    identity = session.identity or "Unknown"

    if world == "One Piece":
        scene = handle_one_piece_phase(session, phase)
    elif world == "Death Note":
        scene = handle_death_note_phase(session, phase)
    else:
        scene = handle_generic_phase(session, phase)

    # Load or initialize chapter
    chapter = load_chapter(world, chapter_num) or {
        "world": world,
        "chapter": chapter_num,
        "entry_mode": entry_mode,
        "scenes": []
    }
    chapter["scenes"].append({
        "phase": phase,
        "narrative": scene
    })
    save_chapter(world, chapter_num, chapter)

    # Final phase check for auto chapter advancement
    final_phases = ["Resolution", "Judgment", "New World"]
    if phase in final_phases:
        actions = [s["narrative"] for s in chapter["scenes"]]
        advance_to_next_chapter(player_id, chapter_num, actions, {"name": world, "tier": session.world_tier}, entry_mode, identity)
        session.current_chapter += 1

    return scene

... (rest unchanged) ...