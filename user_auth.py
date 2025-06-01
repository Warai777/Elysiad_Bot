import json
import os
import bcrypt

USER_FILE = "data/users.json"
PLAYER_DIR = "data/players"

# Ensure files/folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def create_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = {"password": hashed}
    save_users(users)
    
    # Create blank player profile
    profile = {
        "name": username,
        "appearance": "Unknown",
        "personality": [],
        "speech_style": "",
        "origin_essence": 0,
        "worlds_visited": [],
        "suspicion_level": 0
    }
    with open(f"{PLAYER_DIR}/{username}.json", "w") as f:
        json.dump(profile, f, indent=2)

    return True, "User created successfully."

def validate_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    hashed = users[username]["password"].encode()
    if bcrypt.checkpw(password.encode(), hashed):
        return True, "Login successful."
    return False, "Invalid password."

def load_player_profile(username):
    path = f"{PLAYER_DIR}/{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_player_profile(username, profile):
    path = f"{PLAYER_DIR}/{username}.json"
    with open(path, "w") as f:
        json.dump(profile, f, indent=2)