# shard_saver.py
import json
import os

SAVE_DIR = "data/shard_saves"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_shard_state(player_id, session, mission_manager):
    state = {
        "session": session.to_dict(),
        "missions": [vars(m) for m in mission_manager.active_missions]
    }
    with open(f"{SAVE_DIR}/{player_id}_save.json", "w") as f:
        json.dump(state, f)

def load_shard_state(player_id):
    path = f"{SAVE_DIR}/{player_id}_save.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None