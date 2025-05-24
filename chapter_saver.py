import os
import json
from datetime import datetime

CHAPTER_DIR = "data/chapters"

def ensure_chapter_dir():
    os.makedirs(CHAPTER_DIR, exist_ok=True)

def format_narrative(actions):
    if not actions:
        return "The story begins, but the details remain unwritten."
    return " ".join([action[0].upper() + action[1:] if action.endswith('.') else action + '.' for action in actions])

def auto_title(narrative):
    if not narrative.strip():
        return "Untitled Encounter"
    first_sentence = narrative.split('.')[0].strip()
    keywords = first_sentence.split()[:6]
    return " ".join(keywords).capitalize()

def save_chapter_log(player_id, world_data, chapter_num, actions=None, mode="Canon", identity="", entry_time=None):
    ensure_chapter_dir()
    if entry_time is None:
        entry_time = datetime.utcnow().isoformat()

    narrative = format_narrative(actions or [])
    title = auto_title(narrative)
    filename = f"{CHAPTER_DIR}/{player_id}_chapter{chapter_num}.json"
    log_data = {
        "chapter": chapter_num,
        "date": entry_time,
        "world": world_data.get("name"),
        "tier": world_data.get("tier"),
        "mode": mode,
        "identity": identity,
        "title": title,
        "narrative": narrative
    }

    with open(filename, 'w') as f:
        json.dump(log_data, f, indent=4)

def advance_to_next_chapter(player_id, current_chapter, actions, world_data, mode, identity):
    save_chapter_log(
        player_id=player_id,
        world_data=world_data,
        chapter_num=current_chapter,
        actions=actions,
        mode=mode,
        identity=identity
    )
    save_chapter_log(
        player_id=player_id,
        world_data=world_data,
        chapter_num=current_chapter + 1,
        actions=[],
        mode=mode,
        identity=identity
    )