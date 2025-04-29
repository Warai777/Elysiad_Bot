import os
import json
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from player import Player
from genre_manager import GenreManager
from world_manager import WorldManager

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
        chosen_world = request.form["world"]
        world_manager.start_world_timer(player_name, chosen_world)
        return render_template("world_start.html", world=chosen_world, player=player)

    books = world_manager.generate_books()
    return render_template("choose_world.html", books=books, player=player)

if __name__ == "__main__":
    app.run(debug=True)
