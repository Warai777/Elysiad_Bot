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
from starting_scenarios import generate_starting_scenario

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

    if request.method == "POST":
        selected_world_name = request.form.get("world")
        books = session.get("available_books", [])
        chosen_world = next((w for w in books if w["name"] == selected_world_name), None)

        if not chosen_world:
            return redirect(url_for("choose_world"))

        world_manager.start_world_timer(player_name, chosen_world["name"])
        session["current_world"] = chosen_world["name"]
        session["current_world_tone"] = chosen_world["tone"]
        session["current_world_inspiration"] = chosen_world["inspiration"]

        return redirect(url_for("world_scene"))

    # GET request: generate and store the list in session
    books = world_manager.generate_books()
    session["available_books"] = books
    return render_template("choose_world.html", books=books, player=player)

@app.route("/world_scene", methods=["GET", "POST"])
def world_scene():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    
    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    # Archivist Rebirth condition
    if set(player.memory.get("FoundLore", [])) >= set(ARCHIVIST_LORE):
        return redirect(url_for("rebirth_screen"))

    # Handle player choice
    if request.method == "POST":
        selected = int(request.form.get("choice"))
        if session.get("secret_choice") and selected == 6:
            return redirect(url_for("secret_event"))
        if selected == session["death_choice"]:
            return redirect(url_for("death_screen"))
        elif selected == session["progress_choice"]:
            return "<h1>You progress deeper into the world!</h1><a href='/library'>Return</a>"
        elif selected in session["lore_choices"]:
            available_lore = [l for l in ARCHIVIST_LORE if l not in player.memory.get("FoundLore", [])]
            if available_lore:
                found_lore = random.choice(available_lore)
                player.memory.setdefault("FoundLore", []).append(found_lore)
                player.save()
            return redirect(url_for("lore_found_screen"))
        elif selected == session["random_choice"]:
            roll = random.randint(1, 100)
            if roll >= 50:
                adjust_loyalty(player, +5, cause="Survived random danger")
                return "<h1>Good fortune shines on you!</h1><a href='/library'>Return</a>"
            else:
                adjust_loyalty(player, -5, cause="Random misfortune struck")
                return "<h1>Misfortune strikes you...</h1><a href='/library'>Return</a>"

    # Random 20% chance of combat encounter
    if random.random() < 0.2:
        return redirect(url_for("combat"))

    # Generate scene choices
    choices, death, progress, lore, random_c = world_manager.generate_scene_choices()
    session["current_choices"] = choices
    session["death_choice"] = death
    session["progress_choice"] = progress
    session["lore_choices"] = lore
    session["random_choice"] = random_c

    # Track survival time
    survived_minutes = 0
    if player.world_entry_time:
        entry = datetime.datetime.fromisoformat(player.world_entry_time)
        now = datetime.datetime.utcnow()
        survived_minutes = int((now - entry).total_seconds()) // 60
    session["survived_minutes"] = survived_minutes

    # Grit milestones
    milestones = player.memory.setdefault("Milestones", [])
    for minutes, grit_gain, message in [
        (10, 1, "Survived 10 minutes. A faint resilience is born."),
        (30, 2, "Survived 30 minutes. Second Wind awakened."),
        (60, 3, "Survived 60 minutes. Armor of Determination earned."),
        (120, 5, "Survived 120 minutes. Last Stand unlocked — your will transcends death.")
    ]:
        code = f"Milestone{minutes}"
        if survived_minutes >= minutes and code not in milestones:
            milestones.append(code)
            player.grit += grit_gain
            record_memory(player, message)
            player.save()

    # Loyalty bond secret option
    high_loyalty_companions = [c["name"] for c in player.companions if c.get("loyalty", 0) >= 80]
    if high_loyalty_companions:
        session["secret_choice"] = True
        choices.append(f"A mysterious chance... inspired by {random.choice(high_loyalty_companions)}")
    else:
        session["secret_choice"] = False

    # Companion encounter
    companion = companion_manager.random_companion_encounter()
    if companion:
        session["pending_companion"] = companion
        return render_template("companion_encounter.html", companion=companion)

    # Generate immersive scenario description
    from starting_scenarios import generate_starting_scenario
    scenario_text = generate_starting_scenario({
        "name": session.get("current_world"),
        "tone": session.get("current_world_tone"),
        "inspiration": session.get("current_world_inspiration")
    })

    return render_template(
        "world_scene.html",
        player=player,
        world=session.get("current_world"),
        choices=choices,
        survived_minutes=survived_minutes,
        scenario_text=scenario_text
    )

@app.route("/combat", methods=["GET", "POST"])
def combat():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    companions = getattr(player, "companions", [])
    tone = session.get("current_world_tone", "mysterious")
    manager = CombatManager(player, companions, tone)

    if request.method == "POST":
        selected = int(request.form.get("choice"))
        outcome, scar, instinct, assist = manager.resolve_choice(selected)
        if scar:
            player.memory.setdefault("Scars", []).append("Wound from a fierce battle.")
            record_memory(player, "You earned a new mental scar from combat.")
        if instinct:
            player.memory["Instinct"] = player.memory.get("Instinct", 0) + 1
            record_memory(player, "Instinct sharpened by surviving death.")
        player.save()
        return render_template("combat_result.html", outcome=outcome, scar=scar, instinct_gain=instinct, assist_text=assist)

    choices = manager.generate_combat_choices()
    return render_template("combat.html", choices=choices, player=player)

@app.route("/death")
def death_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    if sorted(player.memory.get("FoundLore", [])) == sorted(ARCHIVIST_LORE):
        return redirect(url_for("rebirth_screen"))
    player.memory.setdefault("Deaths", []).append(f"Died inside {player.current_world} after surviving {session.get('survived_minutes', 0)} minutes.")
    for c in player.companions:
        if c.get("loyalty", 0) >= 80:
            record_memory(player, f"You carry the grief of {c['name']} losing you.")
    player.save()
    return render_template("death_screen.html", player=player)

@app.route("/rebirth_screen")
def rebirth_screen():
    player_name = session.get("player_name")
    player = Player.load(player_name)
    return render_template("rebirth.html", player=player)

@app.route("/lore_found")
def lore_found_screen():
    return "<h1>New Lore Discovered!</h1><a href='/world_scene'>Continue</a>"

@app.route("/handle_companion_choice", methods=["POST"])
def handle_companion_choice():
    player_name = session.get("player_name")
    player = Player.load(player_name)
    choice = request.form.get("choice")
    comp = session.get("pending_companion")
    if comp and choice == "accept":
        player.companions.append(comp)
        player.save()
    session.pop("pending_companion", None)
    return redirect(url_for("world_scene"))

@app.route("/secret_event")
def secret_event():
    player = Player.load(session["player_name"])
    record_memory(player, "You shared a bond stronger than fate.")
    adjust_loyalty(player, +10, cause="Forged deep bond through hidden event.")
    return "<h1>A Secret Bond Has Formed...</h1><a href='/world_scene'>Return</a>"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
