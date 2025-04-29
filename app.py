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

    # --- Survival timer ---
    world_entry_time = player.world_entry_time
    if world_entry_time:
        entry_dt = datetime.datetime.fromisoformat(world_entry_time)
        now_dt = datetime.datetime.utcnow()
        survived_seconds = int((now_dt - entry_dt).total_seconds())
        survived_minutes = survived_seconds // 60
    else:
        survived_minutes = 0

    session["survived_minutes"] = survived_minutes

    # --- Grit and Survival Milestones ---
    if survived_minutes >= 10 and "Milestone10" not in player.memory.get("Milestones", []):
        player.memory.setdefault("Milestones", []).append("Milestone10")
        player.grit += 1
        record_memory(player, "Survived 10 minutes. A faint resilience is born.")
        player.save()

    if survived_minutes >= 30 and "Milestone30" not in player.memory.get("Milestones", []):
        player.memory.setdefault("Milestones", []).append("Milestone30")
        player.grit += 2
        record_memory(player, "Survived 30 minutes. Second Wind awakened.")
        player.save()

    if survived_minutes >= 60 and "Milestone60" not in player.memory.get("Milestones", []):
        player.memory.setdefault("Milestones", []).append("Milestone60")
        player.grit += 3
        record_memory(player, "Survived 60 minutes. Armor of Determination earned.")
        player.save()

    if survived_minutes >= 120 and "Milestone120" not in player.memory.get("Milestones", []):
        player.memory.setdefault("Milestones", []).append("Milestone120")
        player.grit += 5
        record_memory(player, "Survived 120 minutes. Last Stand unlocked — your will transcends death.")
        player.save()

    # --- Loyalty Bond Unlock ---
    high_loyalty_companions = []
    for comp in player.companions:
        if comp.get("loyalty", 0) >= 80:
            high_loyalty_companions.append(comp["name"])

    if high_loyalty_companions:
        secret_choice_text = f"A mysterious chance... inspired by {random.choice(high_loyalty_companions)}"
        choices.append(secret_choice_text)
        session["secret_choice"] = True
    else:
        session["secret_choice"] = False

    # --- Companion Encounter Check ---
    companion_encounter = companion_manager.random_companion_encounter()
    if companion_encounter:
        session["pending_companion"] = companion_encounter
        return render_template(
            "companion_encounter.html",
            companion=companion_encounter
        )

    return render_template(
        "world_scene.html",
        player=player,
        world=session.get("current_world"),
        choices=choices,
        survived_minutes=survived_minutes
    )


@app.route("/death")
def death_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    
    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    # 🌟 --- Check if Milestone30 ("Second Wind") saves you ---
    if "Milestone30" in player.memory.get("Milestones", []) and not session.get("second_wind_used", False):
        session["second_wind_used"] = True  # Mark it used
        record_memory(player, "Second Wind triggered — death narrowly avoided!")
        adjust_loyalty(player, +10, cause="Witnessed your miraculous survival.")
        player.save()
        return redirect(url_for("world_scene"))  # ❗️ Send them back into the world alive!

    # 🌟 --- Check if Milestone120 ("Last Stand") saves you ---
    if "Milestone120" in player.memory.get("Milestones", []) and not session.get("last_stand_used", False):
        session["last_stand_used"] = True  # Mark it used
        record_memory(player, "Last Stand activated — willpower defied death itself!")
        adjust_loyalty(player, +15, cause="Felt the shock of your heroic revival.")
        player.save()
        return redirect(url_for("world_scene"))  # ❗️ Survive death once.

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

