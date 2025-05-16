import json
import os
import bcrypt

USER_FILE = "data/users.json"

# Ensure file exists
os.makedirs("data", exist_ok=True)
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
    return True, "User created successfully."

def validate_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    hashed = users[username]["password"].encode()
    if bcrypt.checkpw(password.encode(), hashed):
        return True, "Login successful."
    return False, "Invalid password."