import os
import json
import datetime
import random
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
import openai

# --- CONFIG ---
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
EVENT_INTERVAL = 24 * 60 * 60  # 24 hours

# --- STORAGE ---
USER_FILE = "users.json"
GLOBAL_FILE = "global_state.json"
LORE_FILE = "lore.json"

def load_json(filename, default):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

users = load_json(USER_FILE, {})
global_state = load_json(GLOBAL_FILE, {
    "last_event_time": None,
    "current_event": None,
    "timer": EVENT_INTERVAL
})
lore = load_json(LORE_FILE, [])

def save_users(): save_json(USER_FILE, users)
def save_global(): save_json(GLOBAL_FILE, global_state)
def save_lore(): save_json(LORE_FILE, lore)

# --- GLOBAL EVENT TIMER UTILITY ---
def get_next_event_ts():
    last_event = global_state.get("last_event_time")
    if last_event:
        last_dt = datetime.datetime.fromisoformat(last_event)
        next_event_dt = last_dt + datetime.timedelta(days=1)
        return int(next_event_dt.timestamp())
    else:
        return int(time.time())

# --- USER MODEL ---
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username
        self.data = users[username]

    @property
    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

# --- STORY PROMPT ---
ELY_PROMPT = """
World: Elysiad is a multiverse where anime and web novel worlds overlap.
You are the game master/narrator. The player is a solo human, with no powers, and explores worlds, discovers lore, makes choices, and gradually grows stronger.

Mechanics:
- For each scene, present 5 choices:
  - 1 leads to death (not obvious)
  - 1 progresses story
  - 2 are world-building (lore, bring user back to choose)
  - 1 is random (good/bad by dice roll)
- Roll 1d100: if <50, negative outcome, if >=50, positive.
- Show the result, then present next scene.
- At the end of each scene, summarize key stats: Tier, HP, Origin Essence, Inventory.

Context:
- The world can be affected by current global events: {GLOBAL_EVENT}
- Player's journey so far: {HISTORY}

You must dynamically generate a unique, context-aware chapter name for each scene based on current events, recent choices, or story tone. Format your output as follows at the very top (before the story):

<b>Chapter {CHAPTER}: {CHAPTER_NAME}</b><br>
<b>Scene {SCENE}</b><br>

Then continue with the story and choices. Mark every choice in the output as <b> to make it prominent.
If any new lore is discovered, mention it clearly as: 'Lore Discovered: ...'
"""

def generate_chapter_name(story_context, scene_num):
    themes = ["Lost in the Library", "Chains of Fate", "Shadows in the Hall", "Dawn of Awakening",
              "Call of the Unknown", "A World Unseen", "First Steps", "The Archivist Watches", "The Fateful Choice"]
    if "death" in story_context.lower():
        return "A Narrow Escape"
    if "lore" in story_context.lower():
        return "Secrets Revealed"
    if "choice" in story_context.lower() or scene_num == 1:
        return "First Decision"
    return themes[(scene_num - 1) % len(themes)]

def default_stat_sheet():
    return {
        "Tier": "10-C (Human)",
        "Attack Potency": "Human level",
        "Speed": "Below Average",
        "Durability": "Human level",
        "Stamina": "Average",
        "Range": "Standard melee range",
        "Intelligence": "Average",
        "Standard Equipment": [],
        "Notable Attacks/Techniques": [],
        "Weaknesses": [],
        "HP": 100,
        "Origin Essence": 0,
        "Inventory": [],
        "Story": {"chapter": 1, "scene": 1, "history": [], "recent": [], "started": False, "chapter_names": {}},
        "Lore": [],
        "LastStory": ""
    }

def get_user_data(username):
    if username not in users:
        users[username] = default_stat_sheet()
        save_users()
    return users[username]

def update_recent_action(username, action):
    u = get_user_data(username)
    recent = u['Story'].setdefault("recent", [])
    recent.append(action)
    if len(recent) > 10:
        recent.pop(0)
    save_users()

# --- ROUTES ---
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Username already exists.", "error")
            return redirect(url_for("register"))
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        users[username] = default_stat_sheet()
        users[username]["pw_hash"] = pw_hash
        save_users()
        flash("Registered! Please login.", "info")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and bcrypt.check_password_hash(user["pw_hash"], password):
            login_user(User(username))
            return redirect(url_for("dashboard"))
        else:
            flash("Login failed.", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    u = get_user_data(current_user.username)
    next_event_ts = get_next_event_ts()
    return render_template(
        "dashboard.html",
        user=u,
        global_event=global_state.get("current_event"),
        timer=0,
        users=users,
        history=u['Story'].get("history", []),
        next_event_ts=next_event_ts
    )

@app.route("/char_sheet/<username>")
@login_required
def char_sheet(username):
    if username not in users:
        return "Not found", 404
    u = get_user_data(username)
    next_event_ts = get_next_event_ts()
    return render_template(
        "char_sheet.html",
        user=u,
        username=username,
        global_event=global_state.get("current_event"),
        next_event_ts=next_event_ts
    )

# --- 📖 NEW LORE ROUTE 📖 ---
@app.route("/lore")
@login_required
def lore_index():
    return render_template("lore.html", lore=lore)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
