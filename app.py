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
        selected = request.form.get("choice")
        if selected:  # Player clicked a choice
            selected_choice = int(selected)
            result = session.get("current_choice_result")

            choice_engine = ChoiceEngine()
            choice_engine.generate_choices()

            death_choice = session.get("death_choice")
            progress_choice = session.get("progress_choice")
            lore_choices = session.get("lore_choices")
            random_choice = session.get("random_choice")

            if selected_choice == death_choice:
                return f"<h1>You chose poorly and met your end in {player.current_world}.</h1><a href='/'>Return Home</a>"
            elif selected_choice == progress_choice:
                return f"<h1>You progress deeper into {player.current_world}!</h1><a href='/library'>Return to Library</a>"
            elif selected_choice in lore_choices:
                return f"<h1>You found hidden Lore in {player.current_world}!</h1><a href='/library'>Return to Library</a>"
            elif selected_choice == random_choice:
                roll = random.randint(1, 100)
                if roll >= 50:
                    return f"<h1>You encountered good fortune in {player.current_world}!</h1><a href='/library'>Return to Library</a>"
                else:
                    return f"<h1>Misfortune strikes in {player.current_world}!</h1><a href='/library'>Return to Library</a>"
            else:
                return f"<h1>Invalid choice.</h1><a href='/library'>Return to Library</a>"

        # Otherwise player just landed here
        books = world_manager.generate_books()
        return render_template("choose_world.html", books=books, player=player)

    else:
        # Fresh arrival to choose a world
        choice_engine = ChoiceEngine()
        choice_engine.generate_choices()

        session["current_choices"] = choice_engine.choices
        session["death_choice"] = choice_engine.death_choice
        session["progress_choice"] = choice_engine.progress_choice
        session["lore_choices"] = choice_engine.lore_choices
        session["random_choice"] = choice_engine.random_choice

        books = world_manager.generate_books()
        return render_template("choose_world.html", books=books, player=player)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

