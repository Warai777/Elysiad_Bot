import os
import json
from datetime import datetime

def log_world_entry(player_id, world_data, character_data, entry_mode):
    logs_dir = f"data/chapters/{player_id}/{world_data['world_id']}"
    os.makedirs(logs_dir, exist_ok=True)

    chapter_log = {
        "chapter": 1,
        "date": datetime.utcnow().isoformat() + 'Z',
        "world": world_data['name'],
        "tier": world_data['tier'],
        "entry_mode": entry_mode,
        "identity": character_data['name'],
        "summary": world_data.get('summary', 'No summary available.')
    }

    with open(f"{logs_dir}/chapter1.json", "w") as f:
        json.dump(chapter_log, f, indent=2)
