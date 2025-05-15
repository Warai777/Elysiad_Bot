from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import os, random, time, json
from player import User
from game_session import GameSession
from mission_manager import Mission, MissionManager
from action_handler import ActionHandler
from lore_tracker import LoreTracker
from suspicion_events import check_suspicion_thresholds
from shard_saver import save_shard_state, load_shard_state

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elysiad.db'
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")
db = SQLAlchemy(app)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
reset_codes = {}

player_sessions = {}
mission_managers = {}
lore_trackers = {}
loaded_shard = None

@app.route("/")
def login_page_redirect():
    return redirect(url_for("login_stage"))

@app.route("/login")
def login_stage():
    return render_template("home.html")

@app.route("/login_journal")
def login_page():
    return render_template("login_journal.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["user"] = user.username
        return redirect(url_for("library"))
    flash("Invalid credentials")
    return redirect(url_for("login_page"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        phone = request.form.get("phone")
        username = request.form["username"]
        password = request.form["password"]
        new_user = User(email=email, phone=phone, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login_page"))
    return render_template("signup_page.html")

@app.route("/create_character")
def create_character():
    return render_template("create_character.html")

@app.route("/submit_character", methods=["POST"])
def submit_character():
    global loaded_shard
    name = request.form.get("name")
    background = request.form.get("background")
    trait = request.form.get("trait")
    session["player"] = {"name": name, "background": background, "trait": trait}
    session_id = session["user"]

    # Try loading a save
    saved_state = load_shard_state(session_id)
    if saved_state:
        game_session = GameSession(session_id)
        game_session.load_from_dict(saved_state["session"])
        mission_manager = MissionManager()
        for m in saved_state["missions"]:
            mission = Mission(m["mission_id"], m["description"], m["time_limit"], m["is_main"])
            mission.completed = m["completed"]
            mission.failed = m["failed"]
            mission_manager.add_mission(mission)
        player_sessions[session_id] = game_session
        mission_managers[session_id] = mission_manager
        lore_trackers[session_id] = LoreTracker()
        return redirect(url_for("world_scene"))

    # Fresh run
    player_sessions[session_id] = GameSession(session_id)
    mission_managers[session_id] = MissionManager()
    lore_trackers[session_id] = LoreTracker()

    with open("data/shards/lotm_demo_shard.json") as f:
        loaded_shard = json.load(f)

    main = loaded_shard["main_mission"]
    main_mission = Mission(main["id"], main["description"], 86400, is_main=True)
    mission_managers[session_id].add_mission(main_mission)

    return redirect(url_for("world_scene"))

@app.route("/library")
def library():
    player = session.get("player")
    return render_template("library.html", player=player)

@app.route("/choose_world")
def choose_world():
    return render_template("choose_world.html")

@app.route("/world_scene")
def world_scene():
    global loaded_shard
    if not loaded_shard:
        with open("data/shards/lotm_demo_shard.json") as f:
            loaded_shard = json.load(f)
    return render_template("world_scene.html", shard=loaded_shard)

@app.route("/submit_action", methods=["POST"])
def submit_action():
    session_id = session.get("user")
    data = request.get_json()
    action_text = data.get("action")

    if not session_id or session_id not in player_sessions:
        return jsonify({"error": "No active session"}), 400

    handler = ActionHandler(player_sessions[session_id])
    result = handler.handle_action(action_text, action_type="random")

    # Update lore if critical success
    if result['outcome'] == 'critical_success':
        lore_trackers[session_id].unlock(f"lore_{len(lore_trackers[session_id].unlocked_fragments)+1}")

    # Check suspicion events
    result["suspicion_event"] = check_suspicion_thresholds(player_sessions[session_id])

    # Save progress
    save_shard_state(session_id, player_sessions[session_id], mission_managers[session_id])

    result["session"] = player_sessions[session_id].to_dict()
    result["unlocked_lore"] = lore_trackers[session_id].get_all_unlocked()
    return jsonify(result)

@app.route("/journal")
def journal():
    player_info = session.get("player")
    if not player_info:
        return redirect(url_for("login_page"))

    from player import load_player
    from lore_manager import get_lore_pages, unlock_lore
    from archivist_lore import ARCHIVIST_LORE

    player = load_player(player_info["name"])
    for i in range(len(ARCHIVIST_LORE)):
        unlock_lore(player, i)
    lore_pages = get_lore_pages(player, page_index=0)
    return render_template("journal.html", player=player,
                           left_page=lore_pages["left"], right_page=lore_pages["right"],
                           page_info=lore_pages)

@app.route("/get_lore_page")
def get_lore_page():
    player_info = session.get("player")
    if not player_info:
        return jsonify({"error": "No player found"}), 401

    from player import load_player
    from lore_manager import get_lore_pages, unlock_lore
    from archivist_lore import ARCHIVIST_LORE

    page_index = int(request.args.get("page", 0))
    player = load_player(player_info["name"])
    for i in range(len(ARCHIVIST_LORE)):
        unlock_lore(player, i)
    lore_pages = get_lore_pages(player, page_index=page_index)
    return jsonify({"left": lore_pages["left"], "right": lore_pages["right"],
                    "current_page": lore_pages["current_page"], "total_pages": lore_pages["total_pages"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)