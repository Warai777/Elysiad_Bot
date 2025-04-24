import os
import json
import datetime
import threading
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
import openai

# ========== CONFIG ==========
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client_ai = openai.OpenAI(api_key=OPENAI_API_KEY)
EVENT_INTERVAL = 60 * 60  # 1 hour

# ========== FILE PATHS ==========
USER_FILE = "users.json"
GLOBAL_FILE = "global_state.json"
LORE_FILE = "lore.json"

# ========== STORAGE ==========

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

# ========== USER MODEL ==========
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

# ========== GLOBAL EVENTS ==========
def generate_global_event():
    prompt = (
        "Invent a new global event for a multiverse crossover of anime/webnovel worlds. "
        "Give: Event Name, World(s), and Description (1-2 sentences, no commentary)."
    )
    response = client_ai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        temperature=1.2
    )
    lines = response.choices[0].message.content.splitlines()
    name, world, desc = "Event", "Unknown", ""
    for l in lines:
        if "Event Name:" in l: name = l.split(":",1)[1].strip()
        if "World(s):" in l: world = l.split(":",1)[1].strip()
        if "Description:" in l: desc = l.split(":",1)[1].strip()
    event = f"{name} [{world}]: {desc}"
    global_state["current_event"] = event
    global_state["last_event_time"] = datetime.datetime.utcnow().isoformat()
    save_global()
    print("New global event:", event)
    return event

def next_event_time():
    if not global_state["last_event_time"]:
        return 0
    last = datetime.datetime.fromisoformat(global_state["last_event_time"])
    return (last + datetime.timedelta(seconds=EVENT_INTERVAL) - datetime.datetime.utcnow()).total_seconds()

def time_until_next_event():
    seconds = max(int(next_event_time()), 0)
    return seconds

def auto_event_scheduler():
    while True:
        if next_event_time() <= 0:
            generate_global_event()
        threading.Event().wait(60)

threading.Thread(target=auto_event_scheduler, daemon=True).start()

# ========== STORY ENGINE ==========

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

# ========== ROUTES ==========

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
            flash("Username already exists.")
            return redirect(url_for("register"))
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        users[username] = default_stat_sheet()
        users[username]["pw_hash"] = pw_hash
        save_users()
        flash("Registered! Please login.")
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
            flash("Login failed.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    u = get_user_data(current_user.username)
    message = None

    # --- RANDOMIZED INTRO POOLS ---
    INTRO_TEMPLATES = [
        # SHADOW SLAVE
        "You wake up beneath an iron sky, the taste of bitter sand on your tongue. Chains rattle in the distance. You remember being ordinary—now you are here, lost. A pale door shimmers nearby, inscribed: 'Library of Beginnings.'",
        # LORD OF THE MYSTERIES
        "The city fog was thick, memories of your mundane life fading. You clutch a brass coin, feeling it vibrate with secrets. Then, reality bends, and you stand before the Library of Beginnings, its doors silently inviting you in.",
        # ONE PIECE
        "You dreamed of blue seas and distant laughter. Your small apartment vanishes in a spray of salt air—you find yourself before an ancient, barnacle-crusted Library. Above it, a sign reads: 'Beginnings.'",
        # NARUTO
        "You hear distant village bells. You look down and see a headband—yet not your own. The world blurs and you stand at the edge of a great Library, its stone gates marked with a swirling spiral.",
        # BLEACH
        "A hollow breeze stirs the night. Streetlights flicker; a sword lies at your feet. In the next instant, you stand before the vast Library of Beginnings, its windows glowing faintly in the twilight.",
        # DRAGON BALL
        "You feel a surge of energy—yet it’s gone in an instant. Ordinary once more, you watch as a capsule-shaped object vanishes, revealing a path to the mysterious Library of Beginnings.",
        # STAR WARS
        "You awaken to the hum of distant machinery. A blue glow—like a lightsaber—briefly illuminates a great Library. You step forward; the stars themselves seem to whisper: 'Your story begins here.'",
        # HITCHHIKER'S GUIDE
        "You’re just brushing your teeth when a voice booms: 'Don’t Panic!' Suddenly, you’re standing in front of a vast Library, a towel inexplicably slung over your shoulder. The adventure begins..."
    ]

    # Begin Adventure
    if request.method == "POST" and not u["Story"].get("started", False):
        u["Story"]["started"] = True
        u["Story"]["chapter"] = 1
        u["Story"]["scene"] = 1
        u["Story"]["history"] = []
        u["LastStory"] = ""

        # Pick a random intro
        selected_intro = random.choice(INTRO_TEMPLATES)

        # Now prompt GPT to continue the adventure
        intro_prompt = (
            f"{selected_intro}\n\n"
            "Narrate the scene as a light novel. Immediately follow with a scenario and list FIVE possible actions, numbered. Format strictly as:\n"
            "'Choices:\n1. ...\n2. ...\n3. ...\n4. ...\n5. ...'\n"
            "End your message with the 5 choices, no extras."
        )
        response = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": intro_prompt}],
            max_tokens=700,
            temperature=0.95
        )
        intro = response.choices[0].message.content
        u["LastStory"] = intro
        u["Story"]["history"].append(intro)
        save_users()
        message = intro
        return redirect(url_for("dashboard"))

    # Make a choice
    if request.method == "POST" and u["Story"].get("started", False):
        try:
            number = int(request.form["choice"])
        except:
            flash("Please pick a valid number.")
            return redirect(url_for("dashboard"))
        history = "\n".join(u['Story'].get("history", [])[-5:])
        prompt = ELY_PROMPT.replace("{HISTORY}", history)\
                          .replace("{GLOBAL_EVENT}", global_state.get("current_event") or "None")
        prompt += f"\nCurrent scene: Chapter {u['Story']['chapter']} Scene {u['Story']['scene']}\n"
        prompt += f"User chose: {number}"
        response = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=700,
            temperature=0.95
        )
        story = response.choices[0].message.content
        u['Story']['history'].append(f"<b>Choice {number}:</b> {story}")
        u['LastStory'] = story
        u['Story']['scene'] += 1
        update_recent_action(current_user.username, f"Chose {number}: {story[:120]}...")
        # Lore detection
        if "Lore Discovered:" in story:
            new_lore = story.split("Lore Discovered:", 1)[1].split("\n")[0].strip()
            if new_lore not in lore:
                lore.append(new_lore)
                save_lore()
            if new_lore not in u["Lore"]:
                u["Lore"].append(new_lore)
        save_users()
        message = story

    return render_template(
        "dashboard.html",
        user=u,
        message=message or u["LastStory"],
        global_event=global_state.get("current_event"),
        timer=max(0, int(time_until_next_event())),
        users=users,
        history=u['Story'].get("history", [])
    )

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

@app.route("/timer")
def timer_api():
    return jsonify({"timer": max(0, int(time_until_next_event()))})

    # Generate the intro using GPT-4o (similar to your !start logic)
    intro_prompt = (
        "You are the narrator for a web-based solo adventure in the Elysiad multiverse (anime/web novel worlds crossover). "
        "The player wakes up as a powerless human in a strange multiverse forest. "
        "FIRST: Write only ONE short introduction (max 2 paragraphs). "
        "SECOND: Present a scenario and immediately list FIVE possible actions, each numbered, in the following strict format: "
        "'Choices:\n1. ...\n2. ...\n3. ...\n4. ...\n5. ...' "
        "Include the word 'Choices:' **followed by** the 5 options. "
        "Do NOT output anything after the fifth choice. "
        "NEVER omit the choices. "
        "NEVER output multiple introductions or duplicate text. "
        "Your output MUST always end with 'Choices:' and the five choices."
    )
    response = client_ai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": intro_prompt}],
        max_tokens=700,
        temperature=0.9
    )
    intro = response.choices[0].message.content
    u["LastStory"] = intro
    save_users()
    return redirect(url_for("dashboard"))
# ========== MAIN ==========
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
