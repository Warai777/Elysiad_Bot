import os
import json
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from player import Player, adjust_loyalty, record_memory
from genre_manager import GenreManager
from world_manager import WorldManager
from choice_engine import ChoiceEngine
from companion_manager import CompanionManager
from archivist_lore import ARCHIVIST_LORE
from combat_manager import CombatManager

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
        genre = request.form.get("genre", "Mysterious")
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

    books = world_manager.generate_books()

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

    # --- Check for Archivist Rebirth ---
if set(player.memory.get("Lore", [])) >= set(ARCHIVIST_LORE):
    return redirect(url_for("rebirth"))

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
            found_lore = random.choice(ARCHIVIST_LORE)
            player.memory.setdefault("FoundLore", []).append(found_lore)
            player.save()
            return redirect(url_for('lore_found_screen'))
        elif selected == random_choice:
            roll = random.randint(1, 100)
            if roll >= 50:
                adjust_loyalty(player, +5, cause="Survived random danger")
                return "<h1>Good fortune shines on you!</h1><a href='/library'>Return</a>"
            else:
                adjust_loyalty(player, -5, cause="Random misfortune struck")
                return "<h1>Misfortune strikes you...</h1><a href='/library'>Return</a>"

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

    # --- Milestone Grit Rewards ---
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

    # --- Loyalty bond secret unlock ---
    high_loyalty_companions = [comp["name"] for comp in player.companions if comp.get("loyalty", 0) >= 80]
    if high_loyalty_companions:
        secret_choice_text = f"A mysterious chance... inspired by {random.choice(high_loyalty_companions)}"
        choices.append(secret_choice_text)
        session["secret_choice"] = True
    else:
        session["secret_choice"] = False

    # --- Random Companion Encounter ---
    companion_encounter = companion_manager.random_companion_encounter()
    if companion_encounter:
        session["pending_companion"] = companion_encounter
        return render_template("companion_encounter.html", companion=companion_encounter)

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

    # If player found all Archivist Lore
    found = player.memory.get("FoundLore", [])
    if sorted(found) == sorted(ARCHIVIST_LORE):
        return redirect(url_for("rebirth_screen"))

    # Otherwise: normal death
    cause_of_death = f"Died inside {player.current_world} after surviving {session.get('survived_minutes', 0)} minutes."
    player.memory.setdefault("Deaths", []).append(cause_of_death)

    for comp in player.companions:
        if comp.get("loyalty", 0) >= 80:
            record_memory(player, f"You carry the grief of {comp['name']} losing you.")

    player.save()

    return render_template("death_screen.html", player=player)

@app.route("/rebirth")
def rebirth_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    return render_template("rebirth.html", player=player)

@app.route("/lore_found")
def lore_found_screen():
    return "<h1>New Lore Discovered!</h1><a href='/world_scene'>Continue</a>"

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

    session.pop("pending_companion", None)
    return redirect(url_for("world_scene"))

@app.route("/secret_event")
def secret_event():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))

    player = Player.load(player_name)
    record_memory(player, "You shared a bond stronger than fate.")
    adjust_loyalty(player, +10, cause="Forged deep bond through hidden event.")
    return "<h1>A Secret Bond Has Formed...</h1><a href='/world_scene'>Return</a>"

@app.route("/rebirth")
def rebirth():
    return render_template("rebirth.html")

@app.route("/combat", methods=["GET", "POST"])
def combat():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))

    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    companions = getattr(player, "companions", [])
    world_tone = session.get("current_world_tone", "mysterious")

    combat_manager = CombatManager(player, companions, world_tone)

    if request.method == "POST":
        selected = int(request.form.get("choice"))
        outcome, scar, instinct_gain = combat_manager.resolve_choice(selected)

        # Update player memory and state
        if scar:
            player.memory.setdefault("Scars", []).append("Wound from a fierce battle.")
            record_memory(player, "You earned a new mental scar from combat.")
        if instinct_gain:
            player.memory.setdefault("Instinct", 0)
            player.memory["Instinct"] += 1
            record_memory(player, "Instinct sharpened by surviving death.")

        player.save()

        return render_template(
            "combat_result.html",
            outcome=outcome,
            scar=scar,
            instinct_gain=instinct_gain
        )

    choices = combat_manager.generate_combat_choices()
    return render_template("combat.html", choices=choices, player=player)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
