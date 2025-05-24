import os
import json
from datetime import datetime

CHAPTER_DIR = "data/chapters"

def ensure_chapter_dir():
    os.makedirs(CHAPTER_DIR, exist_ok=True)

def save_chapter_log(player_id, world_data, chapter_num, summary="", mode="Canon", identity="", entry_time=None):
    ensure_chapter_dir()
    if entry_time is None:
        entry_time = datetime.utcnow().isoformat()

    filename = f"{CHAPTER_DIR}/{player_id}_chapter{chapter_num}.json"
    log_data = {
        "chapter": chapter_num,
        "date": entry_time,
        "world": world_data.get("name"),
        "tier": world_data.get("tier"),
        "mode": mode,
        "identity": identity,
        "summary": summary
    }

    with open(filename, 'w') as f:
        json.dump(log_data, f, indent=4)

def generate_chapter_summary(actions):
    """
    Accepts a list of narrative actions, choices, and outcomes from the player.
    Returns a summarized paragraph.
    """
    # Placeholder: real summary logic should parse actions into a coherent recap.
    summary = "In this chapter, you: " + ", then ".join(actions) + "."
    return summary

def advance_to_next_chapter(player_id, current_chapter, actions, world_data, mode, identity):
    summary = generate_chapter_summary(actions)
    save_chapter_log(
        player_id=player_id,
        world_data=world_data,
        chapter_num=current_chapter,
        summary=summary,
        mode=mode,
        identity=identity
    )
    next_chapter = current_chapter + 1
    save_chapter_log(
        player_id=player_id,
        world_data=world_data,
        chapter_num=next_chapter,
        summary="",  # Blank summary until chapter ends
        mode=mode,
        identity=identity
    )