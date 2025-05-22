from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_session import Session
from routes.inventory_routes import inventory_bp
from routes.journal_routes import journal_bp
from routes.save_routes import save_bp
from globals import player_sessions
from game_session import GameSession
from user_auth import create_user, validate_user
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "elysiad-dev")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(inventory_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(save_bp)

@app.route("/")
def index():
    return redirect(url_for("choose_world"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        valid, msg = validate_user(username, password)
        if valid:
            session["user"] = username
            if username not in player_sessions:
                player_sessions[username] = GameSession(username)
            return redirect(url_for("choose_world"))
        else:
            flash(msg)
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password != confirm:
            flash("Passwords do not match.")
        else:
            success, msg = create_user(username, password)
            flash(msg)
            if success:
                return redirect(url_for("login_page"))
    return render_template("signup.html")

@app.route("/choose_world")
def choose_world():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    starter_worlds = [
        {"name": "Harvestland", "inspiration": "The Promised Neverland", "tone": "Grimly hopeful", "summary": "Children hide intelligence behind innocence, waiting for the harvest moon."},
        {"name": "Rosicrucium", "inspiration": "Lord of the Mysteries", "tone": "Mystical, Arcane", "summary": "Ink-bound deities stir beneath the masks of secret societies."},
        {"name": "KameSphere", "inspiration": "Dragon Ball", "tone": "Adventurous, Mythical", "summary": "Chi-infused relics scatter across a world teetering between peace and chaos."},
        {"name": "Seelentiebe", "inspiration": "Dororo", "tone": "Dark redemption", "summary": "A cursed body hunts demons to reclaim what was bartered away."},
        {"name": "Chrysalis", "inspiration": "Worm", "tone": "Hopeful despair", "summary": "Every power bears a price in a city drowning in consequence."},
        {"name": "AeonRebirth", "inspiration": "Evangelion", "tone": "Post-apocalyptic, Existential", "summary": "Pilots dream of peace while carrying the weight of shattered gods."},
        {"name": "IronArc", "inspiration": "Fullmetal Alchemist", "tone": "Industrial magic", "summary": "Alchemy fuels a war machine that may devour its own soul."},
        {"name": "Nullspire", "inspiration": "Made in Abyss", "tone": "Surreal horror", "summary": "A chasm of dreams tempts explorers to depths no mind can endure."},
        {"name": "Blightvale", "inspiration": "Bloodborne", "tone": "Victorian grotesque", "summary": "Ink, beasts, and madness soak the cobblestones under twin moons."},
        {"name": "Skysteel", "inspiration": "Stormlight Archive", "tone": "Mythic conflict", "summary": "Ancient oaths awaken as highstorms carve the battlefield skies."}
    ]

    return render_template("choose_world.html", worlds=starter_worlds)

@app.route("/enter_world", methods=["POST"])
def enter_world():
    selected_world = request.form.get("world")
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    current_session = player_sessions[session_id]
    current_session.current_world = selected_world
    current_session.log_journal(f"You have entered the world of {selected_world}.", type_="system", importance="high", tags=["world"])
    return redirect(url_for("world_scene"))

@app.route("/world_scene", methods=["GET", "POST"])
def world_scene():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    current_session = player_sessions[session_id]
    current_session.autosave_if_needed()
    story_text = ""
    if request.method == "POST":
        from story_manager import generate_story_scene
        story_text = generate_story_scene(current_session)
    return render_template("world_scene.html", session=current_session, story_text=story_text)

@app.route("/examine_item", methods=["POST"])
def examine_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    item_name = request.form.get("item")
    session_data = player_sessions[session_id]
    item = next((i for i in session_data.inventory if i["name"] == item_name and i.get("type") == "mystery"), None)

    if item:
        result = session_data.reveal_items()
        if item_name in result:
            flash(f"You deciphered {item_name}!")
        else:
            flash("You examine it carefully but learn nothing yet.")
    else:
        flash("That item cannot be examined.")
    return redirect(url_for("inventory_bp.inventory"))

if __name__ == "__main__":
    app.run(debug=True)