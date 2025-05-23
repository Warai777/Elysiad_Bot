import os, json
from datetime import datetime

def save_chapter(world_name, chapter_number, content):
    os.makedirs(f"data/chapters/{world_name}", exist_ok=True)
    with open(f"data/chapters/{world_name}/chapter{chapter_number}.json", "w") as f:
        json.dump(content, f, indent=2)

def load_chapter(world_name, chapter_number):
    path = f"data/chapters/{world_name}/chapter{chapter_number}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def log_world_entry(world, profile, mode):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "world": world["name"],
        "tier": world["tier"],
        "entry_mode": mode,
        "identity": world["canon_profile"] if mode == "canon" else profile,
        "summary": world["summary"]
    }
    save_chapter(world["name"], 1, entry)