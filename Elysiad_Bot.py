from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import openai
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "elysiad_secret"
login_manager = LoginManager(app)
login_manager.login_view = "login"

USER_FILE = "users.json"
LORE_FILE = "lore.json"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client_ai = openai.OpenAI(api_key=OPENAI_API_KEY)

def load_json(filename, default):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

class Player(UserMixin):
    def __init__(self, username):
        self.id = username
        self.data = load_json(USER_FILE, {}).get(username)

    @staticmethod
    def get(username):
        users = load_json(USER_FILE, {})
        if username in users:
            return Player(username)
        return None

    def save(self):
        users = load_json(USER_FILE, {})
        users[self.id] = self.data
        save_json(USER_FILE, users)

@login_manager.user_loader
def load_user(user_id):
    return Player.get(user_id)

def create_user(username, password):
    users = load_json(USER_FILE, {})
    if username in users:
        return False
    users[username] = {
        "password": generate_password_hash(password),
        "Name": username,
        "Tier": "10-C (Human)",
        "HP": 100,
        "Origin Essence": 0,
        "Inventory": [],
        "LoreFound": [],
        "Story": {"chapter": 1, "scene": 1, "history": [], "started": False},
        "LastStory": ""
    }
    save_json(USER_FILE, users)
    return True

def check_user(username, password):
    users = load_json(USER_FILE, {})
    user = users.get(username)
    if user and check_password_hash(user["password"], password):
        return True
    return False

def add_lore_entry(lore_text, discoverer):
    lore = load_json(LORE_FILE, [])
    if lore_text not in [entry["text"] for entry in lore]:
        lore.append({"text": lore_text, "by": discoverer})
        save_json(LORE_FILE, lore)

def get_lore():
    return load_json(LORE_FILE, [])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if create_user(username, password):
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
        else:
            flash("Username already exists.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_user(username, password):
            user = Player.get(username)
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    user = current_user
    data = user.data
    # Start or continue
    if not data["Story"]["started"]:
        intro_prompt = (
            "You are the narrator for a browser solo adventure game. "
            "The player wakes up as a powerless human in a strange multiverse forest. "
            "FIRST: Write only ONE short introduction (max 2 paragraphs). "
            "SECOND: Present a scenario and immediately list FIVE possible actions, each numbered, in this strict format: "
            "'Choices:\n1. ...\n2. ...\n3. ...\n4. ...\n5. ...' "
            "Do NOT output anything after the fifth choice. "
            "NEVER output multiple introductions or duplicate text. "
            "Your output MUST always end with 'Choices:' and the five choices."
        )
        response = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": intro_prompt}],
            max_tokens=700,
            temperature=0.9
        )
        story = response.choices[0].message.content
        data["LastStory"] = story
        data["Story"]["started"] = True
        user.save()
    else:
        story = data["LastStory"]

    # Parse choices
    choices = []
    lore_discovered = []
    if "Choices:" in story:
        before, choices_block = story.split("Choices:", 1)
        for line in choices_block.strip().split("\n"):
            if "Lore Discovered:" in line:
                lore = line.split("Lore Discovered:",1)[1].strip()
                lore_discovered.append(lore)
                add_lore_entry(lore, data["Name"])
            elif line.strip() and line.strip()[0].isdigit():
                choices.append(line.strip())
    else:
        before = story

    return render_template("web_adventure.html", user=data, story=before, choices=choices, lore_discovered=lore_discovered, lore_index=get_lore())

@app.route("/choose/<int:num>")
@login_required
def choose(num):
    user = current_user
    data = user.data
    history = "\n".join(data['Story'].get("history", [])[-5:])
    prompt = f"""
    World: Elysiad is a multiverse where anime and web novel worlds overlap.
    You are the game master/narrator. The player is a solo human, with no powers, and explores worlds, discovers lore, makes choices, and gradually grows stronger.
    Mechanics:
    - For each scene, present 5 choices:
      - 1 leads to death (not obvious)
      - 1 progresses story
      - 2 are world-building (lore, bring user back to choose)
      - 1 is random (good/bad by dice roll)
    - If the user discovers new lore, add 'Lore Discovered: <lore fact>' to the end of your output.
    - Roll 1d100: if <50, negative outcome, if >=50, positive.
    - Show the result, then present next scene.
    - At the end of each scene, summarize key stats: Tier, HP, Origin Essence, Inventory.
    Player's journey so far: {history}
    Current scene: Chapter {data['Story']['chapter']} Scene {data['Story']['scene']}
    User chose: {num}
    Respond in a light-novel style.
    Present next set of 5 choices at the end of the message (list as "Choices: 1. ... 2. ... etc.")
    NEVER repeat the choices or intro more than once. Do not send duplicate scenes.
    """

    response = client_ai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=700,
        temperature=0.95
    )
    story = response.choices[0].message.content
    data['Story']['history'].append(f"Choice {num}: {story[:150]}...")
    data['LastStory'] = story
    data['Story']['scene'] += 1
    # Check for lore in story
    if "Lore Discovered:" in story:
        for line in story.splitlines():
            if "Lore Discovered:" in line:
                lore_fact = line.split("Lore Discovered:",1)[1].strip()
                add_lore_entry(lore_fact, data["Name"])
    user.save()
    return redirect(url_for('home'))

@app.route("/lore")
@login_required
def lore():
    lore = get_lore()
    return render_template("lore_index.html", lore=lore)

@app.route("/stats")
@login_required
def stats():
    data = current_user.data
    return render_template("stat_sheet.html", user=data)

if __name__ == "__main__":
    app.run(debug=True)
