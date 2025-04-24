import os, json, datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client_ai = openai.OpenAI(api_key=OPENAI_API_KEY)

USER_FILE = "users.json"
LORE_FILE = "lore.json"
GLOBAL_FILE = "global_state.json"

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
lore = load_json(LORE_FILE, [])
global_state = load_json(GLOBAL_FILE, {
    "last_event_time": None,
    "current_event": None,
})

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

def get_user(username):
    if username not in users:
        users[username] = {
            "username": username,
            "password": "",
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
            "Story": {"chapter": 1, "scene": 1, "history": [], "started": False},
            "LastStory": ""
        }
        save_json(USER_FILE, users)
    return users[username]

def save_users(): save_json(USER_FILE, users)
def save_lore(): save_json(LORE_FILE, lore)
def save_global(): save_json(GLOBAL_FILE, global_state)

# GLOBAL EVENT HANDLER
def get_global_event():
    return global_state.get("current_event", "")

def set_global_event(event):
    global_state["current_event"] = event
    global_state["last_event_time"] = datetime.datetime.utcnow().isoformat()
    save_global()

def next_event_time():
    if not global_state["last_event_time"]:
        return 0
    last = datetime.datetime.fromisoformat(global_state["last_event_time"])
    return (last + datetime.timedelta(hours=1) - datetime.datetime.utcnow()).total_seconds()

def seconds_to_clock(secs):
    m = secs // 60
    s = secs % 60
    return f"{m}:{s:02d}"

# --- ROUTES ---
@app.route("/")
def root():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        u = users.get(username)
        if u and bcrypt.check_password_hash(u["password"], password):
            user_obj = User(username)
            login_user(user_obj)
            session["user_id"] = username
            return redirect("/dashboard")
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            error = "Username already exists."
        else:
            hashed = bcrypt.generate_password_hash(password).decode("utf-8")
            users[username] = get_user(username)
            users[username]["password"] = hashed
            save_users()
            return redirect("/login")
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    logout_user()
    session.pop("user_id", None)
    return redirect("/login")

@app.route("/dashboard")
@login_required
def dashboard():
    user_objs = [users[u] for u in users]
    event = get_global_event()
    return render_template("dashboard.html",
        users=user_objs,
        global_event=event,
        time_left=seconds_to_clock(max(int(next_event_time()),0))
    )

@app.route("/stat_sheet/<username>")
@login_required
def stat_sheet(username):
    user = users.get(username)
    if not user:
        return "User not found", 404
    return render_template("stat_sheet.html", user=user)

@app.route("/lore_index")
@login_required
def lore_index():
    return render_template("lore_index.html", lore=lore)

@app.route("/adventure", methods=["GET", "POST"])
@login_required
def adventure():
    user = get_user(current_user.username)
    if not user["Story"]["started"]:
        # Get intro from GPT
        prompt = (
            "You are the narrator for a web-based solo adventure. The player wakes as a powerless human in a strange multiverse. "
            "FIRST: Give a short introduction (max 2 paragraphs). "
            "SECOND: Present a scenario and list FIVE possible actions, numbered 1-5, as: 'Choices:\\n1. ...\\n2. ...\\n3. ...\\n4. ...\\n5. ...'"
            "Your output MUST end with 'Choices:' and the five choices. NEVER duplicate or repeat text or output more than once."
        )
        response = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=700,
            temperature=0.9
        )
        story = response.choices[0].message.content
        user["Story"]["started"] = True
        user["LastStory"] = story
        save_users()
        return render_template("web_adventure.html", story=story)
    else:
        if request.method == "POST":
            choice = request.form["choice"]
            history = "\n".join(user["Story"].get("history", [])[-5:])
            prompt = f"""World: Elysiad is a multiverse where anime and web novel worlds overlap.
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
- The world can be affected by current global events: {get_global_event()}
- Player's journey so far: {history}

Current scene: Chapter {user['Story']['chapter']} Scene {user['Story']['scene']}
User chose: {choice}
Respond in a light-novel style.
Present next set of 5 choices at the end of the message (list as "Choices: 1. ... 2. ... etc.")
NEVER repeat choices or the intro.
"""
            response = client_ai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=700,
                temperature=0.95
            )
            story = response.choices[0].message.content
            user['Story']['history'].append(f"Choice {choice}: {story[:200]}...")
            user['LastStory'] = story
            user['Story']['scene'] += 1
            save_users()
            # LORE DISCOVERY (Example): Add logic to detect new lore in story and update lore.json
            if "LORE:" in story:  # crude example
                entry = {
                    "title": f"Lore from {user['username']}",
                    "content": story.split("LORE:")[1].split("\n")[0],
                    "found_by": user["username"],
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }
                lore.append(entry)
                save_lore()
            return render_template("web_adventure.html", story=story)
        return render_template("web_adventure.html", story=user["LastStory"])

if __name__ == "__main__":
    app.run(debug=True)
