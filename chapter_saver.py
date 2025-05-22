import os
import json

CHAPTER_DIR = "data/chapters"

if not os.path.exists(CHAPTER_DIR):
    os.makedirs(CHAPTER_DIR)

def save_chapter(world_name, chapter_number, chapter_data):
    filename = f"{world_name}_Chapter_{chapter_number}.json"
    filepath = os.path.join(CHAPTER_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(chapter_data, f, indent=2)

def load_chapter(world_name, chapter_number):
    filename = f"{world_name}_Chapter_{chapter_number}.json"
    filepath = os.path.join(CHAPTER_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return json.load(f)

def list_chapters():
    return [f for f in os.listdir(CHAPTER_DIR) if f.endswith(".json")]