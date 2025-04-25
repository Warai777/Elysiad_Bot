import os
import json
import datetime
import threading
import random
import time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, Response, stream_with_context
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

Respond in a detailed and thought-out light-novel style.
Present next set of 5 choices at the end of the message (list as "Choices: 1. ... 2. ... etc.")
If any new lore is discovered, mention it clearly as: 'Lore Discovered: ...'
"""

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
        "Story": {"chapter": 1, "scene": 1, "history": [], "recent": [], "started": False},
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
    last_event = global_state.get("last_event_time")
    if last_event:
        last_dt = datetime.datetime.fromisoformat(last_event)
        next_event_dt = last_dt + datetime.timedelta(days=1)
        next_event_ts = int(next_event_dt.timestamp())
    else:
        next_event_ts = int(time.time())

    return render_template(
        "dashboard.html",
        user=u,
        global_event=global_state.get("current_event"),
        timer=0,
        users=users,
        history=u['Story'].get("history", []),
        next_event_ts=next_event_ts
    )

@app.route("/stream_story", methods=["POST"])
@login_required
def stream_story():
    u = get_user_data(current_user.username)

    def stream_openai_response(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            stream=True,
            max_tokens=700,
            temperature=0.95,
        )
        full_story = ""
        for chunk in response:
            content = chunk['choices'][0].get('delta', {}).get('content')
            if content:
                full_story += content
                yield content
        # Save story after stream done
        if "Lore Discovered:" in full_story:
            new_lore = full_story.split("Lore Discovered:", 1)[1].split("\n")[0].strip()
            if new_lore not in lore:
                lore.append(new_lore)
                save_lore()
            if new_lore not in u["Lore"]:
                u["Lore"].append(new_lore)
        if not u["Story"].get("started"):
            u["Story"]["started"] = True
        u["Story"]["history"].append(full_story)
        u["LastStory"] = full_story
        u["Story"]["scene"] += 1
        save_users()

    # New game/intro or next choice
    if request.form.get("begin") == "1":
        INTRO_TEMPLATES = [
            "You wake up beneath an iron sky, the taste of bitter sand on your tongue. Chains rattle in the distance. You remember being ordinary—now you are here, lost. A pale door shimmers nearby, inscribed: 'Library of Beginnings.'",
            # ...add more intros if you wish...
        ]
        selected_intro = random.choice(INTRO_TEMPLATES)
        prompt = (
            f"{selected_intro}\n\n"
            "Narrate the scene as a light novel. Immediately follow with a scenario and list FIVE possible actions, numbered. Format strictly as:\n"
            "'Choices:\n1. ...\n2. ...\n3. ...\n4. ...\n5. ...'\n"
            "End your message with the 5 choices, no extras."
        )
        u["Story"]["started"] = True
        u["Story"]["chapter"] = 1
        u["Story"]["scene"] = 1
        u["Story"]["history"] = []
        u["LastStory"] = ""
        save_users()
    else:
        try:
            number = int(request.form["choice"])
        except:
            number = 1
        history = "\n".join(u['Story'].get("history", [])[-5:])
        prompt = ELY_PROMPT.replace("{HISTORY}", history)\
            .replace("{GLOBAL_EVENT}", global_state.get("current_event") or "None")
        prompt += f"\nCurrent scene: Chapter {u['Story']['chapter']} Scene {u['Story']['scene']}\n"
        prompt += f"User chose: {number}"

    return Response(stream_with_context(stream_openai_response(prompt)), mimetype='text/plain')

@app.route("/char_sheet/<username>")
@login_required
def char_sheet(username):
    if username not in users:
        return "Not found", 404
    u = get_user_data(username)
    return render_template("char_sheet.html", user=u, username=username)

@app.route("/lore")
@login_required
def lore_index():
    return render_template("lore_index.html", lore=lore)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
