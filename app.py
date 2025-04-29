import os
import json
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from player import Player
from genre_manager import GenreManager
from world_manager import WorldManager
from choice_engine import ChoiceEngine

# --- CONFIG ---
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "elysiad_secret_key")

# --- SETUP ---
genre_manager = GenreManager()
world_manager = WorldManager()

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
    return render_template("library.html", player=player)

@app.route("/choose_world", methods=["GET", "POST"])
def choose_world():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)

    if request.method == "POST":
        chosen_world = request.form.get("world")
        if chosen_world:
            world_manager.start_world_timer(player_name, chosen_world)
            session["current_world"] = chosen_world
            return redirect(url_for("world_scene"))
    else:
        books = world_manager.generate_books()
        return render_template("choose_world.html", books=books, player=player)

@app.route("/world_scene", methods=["GET", "POST"])
def world_scene():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)

    if request.method == "POST":
        selected = int(request.form.get("choice"))
        death_choice = session.get("death_choice")
        progress_choice = session.get("progress_choice")
        lore_choices = session.get("lore_choices")
        random_choice = session.get("random_choice")

        if selected == death_choice:
            return redirect(url_for('death_screen'))
        elif selected == progress_choice:
            return "<h1>You progress deeper into the world!</h1><a href='/library'>Return</a>"
        elif selected in lore_choices:
            return redirect(url_for('lore_found_screen'))
        elif selected == random_choice:
            roll = random.randint(1, 100)
            if roll >= 50:
                return "<h1>Good fortune shines on you!</h1><a href='/library'>Return</a>"
            else:
                return "<h1>Misfortune strikes you...</h1><a href='/library'>Return</a>"
        else:
            return "<h1>Invalid choice.</h1><a href='/library'>Return</a>"

    # ⬇️⬇️⬇️ NOT `else:` HERE! Just continue normally!
    
    # This happens if request.method == "GET"
    choices, death, progress, lore, random_c = world_manager.generate_scene_choices()
    session["current_choices"] = choices
    session["death_choice"] = death
    session["progress_choice"] = progress
    session["lore_choices"] = lore
    session["random_choice"] = random_c

    world_entry_time = player.world_entry_time
    if world_entry_time:
        entry_dt = datetime.datetime.fromisoformat(world_entry_time)
        now_dt = datetime.datetime.utcnow()
        survived_seconds = int((now_dt - entry_dt).total_seconds())
        survived_minutes = survived_seconds // 60
    else:
        survived_minutes = 0

    session["survived_minutes"] = survived_minutes

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

    # Save death memory
    cause_of_death = f"Died inside {player.current_world} after surviving {session.get('survived_minutes', 0)} minutes."
    player.memory.setdefault("Deaths", []).append(cause_of_death)
    player.save()

    return render_template("death_screen.html", player=player)

@app.route("/lore_found")
def lore_found_screen():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("home"))
    player = Player.load(player_name)
    return render_template("lore_found.html", player=player)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

