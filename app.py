import os
import json
import random
import datetime
import openai

from flask import Flask, render_template, request, redirect, url_for, session
from player import Player, adjust_loyalty, record_memory
from genre_manager import GenreManager
from world_manager import WorldManager
from choice_engine import ChoiceEngine
from companion_manager import generate_ai_inspired_companion
from archivist_lore import ARCHIVIST_LORE
from story_manager import StoryManager
from combat_manager import CombatManager

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "elysiad_secret_key")

# Set up managers
genre_manager = GenreManager()
world_manager = WorldManager()
story_engine = StoryManager(ai_model="gpt-4")

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
    journal = player.memory.get("Journal", {})
    return render_template("library.html", player=player, companions=companions, journal=journal)

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
        session["scene_initialized"] = False  # Reset the combat trigger
        return redirect(url_for("world_scene"))

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

    if set(player.memory.get("FoundLore", [])) >= set(ARCHIVIST_LORE):
        return redirect(url_for("rebirth_screen"))

    if request.method == "POST":
        selected = int(request.form.get("choice"))
        if session.get("secret_choice") and selected == 6:
            return redirect(url_for("secret_event"))
        elif selected == session["death_choice"]:
            return redirect(url_for("death_screen"))
        elif selected == session["progress_choice"]:
            return "<h1>You progress deeper into the world!</h1><a href='/library'>Return</a>"
        elif selected in session["lore_choices"]:
            available = [l for l in ARCHIVIST_LORE if l not in player.memory.get("FoundLore", [])]
            if available:
                found = random.choice(available)
                player.memory.setdefault("FoundLore", []).append(found)
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

    # Track survival time
    survived_minutes = 0
    if player.world_entry_time:
        try:
            entry = datetime.datetime.fromisoformat(player.world_entry_time)
            now = datetime.datetime.utcnow()
            survived_minutes = int((now - entry).total_seconds()) // 60
        except Exception:
            survived_minutes = 0
    session["survived_minutes"] = survived_minutes

    # Check for high-loyalty companions
    high_loyalty = [c["name"] for c in player.companions if c.get("loyalty", 0) >= 80]
    session["secret_choice"] = bool(high_loyalty)

    # Companion encounter override (replaces tone-based with AI-based logic)
    world_inspiration = session.get("current_world_inspiration")
    companion = generate_ai_inspired_companion(world_inspiration)
    if companion:
        session["pending_companion"] = companion
        return render_template("companion_encounter.html", companion=companion)


    # Determine narrative phase
    phase = "Intro" if survived_minutes < 1 else "Exploration"

    # ✅ Generate story and choices
    scenario_text, contextual_choices = story_engine.generate_story_segment(
        world={
            "name": session.get("current_world", "Unknown"),
            "inspiration": session.get("current_world_inspiration", "Original")
        },
        tone=session.get("current_world_tone", "mystical"),
        player_traits=player.traits,
        player_memory=player.memory,
        companions=player.companions,
        phase=phase
    )

    # ✅ Check for combat triggers in story content
    combat_keywords = [
        "ambush", "attack", "enemy", "draw your weapon", "hostile", "creature snarls",
        "a fight begins", "battle erupts", "you are not alone", "lunges at you", "prepare to fight"
    ]

    if any(kw in scenario_text.lower() for kw in combat_keywords):
        session["pending_combat_story"] = scenario_text  # Save story for combat display
        return redirect(url_for("combat"))

    # Setup choices
    choices = [(i + 1, choice) for i, choice in enumerate(contextual_choices[:5])]
    session["death_choice"] = 1
    session["progress_choice"] = 2
    session["lore_choices"] = [3]
    session["random_choice"] = 4
    if session.get("secret_choice"):
        choices.append((6, f"A mysterious chance... inspired by {random.choice(high_loyalty)}"))
    session["current_choices"] = choices

    return render_template(
        "world_scene.html",
        player=player,
        world=session.get("current_world", "Unknown"),
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
    if not player:
        return redirect(url_for("home"))

    pending_story = session.get("pending_combat_story", "A shadow looms... but you can't recall how it began.")

    if request.method == "POST":
        selected_index = int(request.form.get("choice"))  # 0-based
        manager = CombatManager(player, player.companions, session.get("current_world_tone", "neutral"))
        narrative, scar_text, instinct_text, assist_text = manager.resolve_choice(selected_index)

        return render_template(
            "combat_result.html",
            player=player,
            narrative=narrative,
            scar_text=scar_text,
            instinct_text=instinct_text,
            assist_text=assist_text
        )

    manager = CombatManager(player, player.companions, session.get("current_world_tone", "neutral"))
    choices = manager.generate_combat_choices()

    return render_template(
        "combat.html",
        player=player,
        opening_story=pending_story,
        choices=enumerate(choices)
    )


@app.route("/rebirth_screen")
def rebirth_screen():
    player_name = session.get("player_name")
    player = Player.load(player_name)
    return render_template("rebirth.html", player=player)

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
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    record_memory(player, "You shared a bond stronger than fate.")
    adjust_loyalty(player, +10, cause="Forged deep bond through hidden event.")
    return "<h1>A Secret Bond Has Formed...</h1><a href='/world_scene'>Return</a>"

@app.route("/journal")
def view_journal():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    journal = player.memory.get("Journal", {
        "Hints": [],
        "Lore": [],
        "Events": [],
        "Notes": []
    })
    return render_template("journal.html", player=player, journal=journal)

@app.route("/add_note", methods=["POST"])
def add_note():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    note = request.form.get("note", "").strip()
    if note:
        player.memory.setdefault("Journal", {}).setdefault("Notes", []).append(note)
        player.save()
    return redirect(url_for("view_journal"))

@app.route("/death_screen", methods=["GET"])
def death_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))

    player = Player.load(player_name)
    if not player:
        return redirect(url_for("home"))

    return render_template("death_screen.html", player=player)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
