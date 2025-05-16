from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_session import Session
from routes.inventory_routes import inventory_bp
from routes.journal_routes import journal_bp
from routes.save_routes import save_bp
from game_session import GameSession
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "elysiad-dev")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Register blueprints
app.register_blueprint(inventory_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(save_bp)

# Global session tracker
player_sessions = {}

@app.route("/")
def index():
    return redirect(url_for("world_scene"))

@app.route("/login")
def login_page():
    return render_template("login.html")

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