import os
import json
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from player import Player
from genre_manager import GenreManager
from world_manager import WorldManager
from choice_engine import ChoiceEngine
from companion_manager import CompanionManager
from archivist_lore import ARCHIVIST_LORE

# --- CONFIG ---
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "elysiad_secret_key")

# --- SETUP ---
genre_manager = GenreManager()
world_manager = WorldManager()
companion_manager = CompanionManager()

# --- ROUTES ---

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_character", methods=["GET", "POST"])
def create_character():
    if request.method == "POST":
        name = request.form["name"]
        background = request.form["background"]
        genre = request.form.get("genre", "Mysterious")  # Default if none picked
        player = Player(name, background, genre)
        player.save()
        session["player_name"] = name
        return redirect(url_for("library"))
    return render_template("create_character.html", genres=genre_manager.available_genres)

@app.route("/library")
def library():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))

    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    companions = getattr(player, "companions", [])

    return render_template("library.html", player=player, companions=companions)

@app.route("/choose_world", methods=["GET", "POST"])
def choose_world():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    
    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    books = world_manager.generate_books()  # Moved this to the top

    if request.method == "POST":
        selected_world_name = request.form.get("world")
        chosen_world = next((w for w in books if w["name"] == selected_world_name), None)

        if not chosen_world:
            return redirect(url_for("choose_world"))

        world_manager.start_world_timer(player_name, chosen_world["name"])
        session["current_world"] = chosen_world["name"]
        session["current_world_tone"] = chosen_world["tone"]
        session["current_world_inspiration"] = chosen_world["inspiration"]

        return redirect(url_for("world_scene"))

    return render_template("choose_world.html", books=books, player=player)

@app.route("/world_scene", methods=["GET", "POST"])
def world_scene():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    
    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    if request.method == "POST":
        selected = int(request.form.get("choice"))
        death_choice = session.get("death_choice")
        progress_choice = session.get("progress_choice")
        lore_choices = session.get("lore_choices")
        random_choice = session.get("random_choice")
        secret_unlocked = session.get("secret_choice", False)

        if secret_unlocked and selected == 6:
            return redirect(url_for("secret_event"))

        if selected == death_choice:
            return redirect(url_for('death_screen'))
        elif selected == progress_choice:
            return "<h1>You progress deeper into the world!</h1><a href='/library'>Return</a>"
        elif selected in lore_choices:
            return redirect(url_for('lore_found_screen'))
        elif selected == random_choice:
            roll = random.randint(1, 100)
            if roll >= 50:
                adjust_loyalty(player, +5, cause="Survived random danger")
                return "<h1>Good fortune shines on you!</h1><a href='/library'>Return</a>"
            else:
                adjust_loyalty(player, -5, cause="Random misfortune struck")
                return "<h1>Misfortune strikes you...</h1><a href='/library'>Return</a>"

    # --- Normal choice generation ---
    choices, death, progress, lore, random_c = world_manager.generate_scene_choices()
    session["current_choices"] = choices
    session["death_choice"] = death
    session["progress_choice"] = progress
    session["lore_choices"] = lore
    session["random_choice"] = random_c

   # --- Survival Timer ---
world_entry_time = player.world_entry_time
survived_minutes = 0

if world_entry_time:
    entry_dt = datetime.datetime.fromisoformat(world_entry_time)
    now_dt = datetime.datetime.utcnow()
    survived_seconds = int((now_dt - entry_dt).total_seconds())
    survived_minutes = survived_seconds // 60

session["survived_minutes"] = survived_minutes

# --- Milestone Achievements ---
milestones = player.memory.setdefault("Milestones", [])

milestone_events = [
    (10, 1, "Survived 10 minutes. A faint resilience is born."),
    (30, 2, "Survived 30 minutes. Second Wind awakened."),
    (60, 3, "Survived 60 minutes. Armor of Determination earned."),
    (120, 5, "Survived 120 minutes. Last Stand unlocked — your will transcends death.")
]

for minutes, grit_gain, message in milestone_events:
    code = f"Milestone{minutes}"
    if survived_minutes >= minutes and code not in milestones:
        milestones.append(code)
        player.grit += grit_gain
        record_memory(player, message)
        player.save()

    # --- Otherwise: you really die ---
    cause_of_death = f"Died inside {player.current_world} after surviving {session.get('survived_minutes', 0)} minutes."
    player.memory.setdefault("Deaths", []).append(cause_of_death)

    # Emotional impact for companions
    for comp in player.companions:
        if comp.get("loyalty", 0) >= 80:
            record_memory(player, f"You carry the grief of {comp['name']} losing you.")

    player.save()

    return render_template("death_screen.html", player=player)

@app.route("/lore_found")
def lore_found_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    return render_template("lore_found.html", player=player)

@app.route("/handle_companion_choice", methods=["POST"])
def handle_companion_choice():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))

    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    choice = request.form.get("choice")
    companion = session.get("pending_companion")

    if companion and choice == "accept":
        if not hasattr(player, "companions"):
            player.companions = []
        player.companions.append(companion)
        player.save()

    # Always remove from session (accepted or rejected)
    session.pop("pending_companion", None)

    return redirect(url_for("world_scene"))

@app.route("/secret_event")
def secret_event():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)

    # 🌟 Add a powerful hidden memory
    record_memory(player, "You shared a bond stronger than fate.")

    # 🌟 Loyalty boost for all companions
    adjust_loyalty(player, +10, cause="Forged deep bond through hidden event.")

    return render_template("secret_event.html", player=player)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

