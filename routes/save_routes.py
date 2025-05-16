from flask import Blueprint, request, session, redirect, url_for, render_template
from game_session import GameSession

save_bp = Blueprint("save_bp", __name__)

save_slots = {}  # Dictionary to store named sessions keyed by user

@save_bp.route("/saves")
def show_saves():
    user_id = session.get("user")
    slots = save_slots.get(user_id, {})
    return render_template("saves.html", slots=slots)

@save_bp.route("/create_save", methods=["POST"])
def create_save():
    user_id = session.get("user")
    slot_name = request.form.get("slot_name")
    if user_id and slot_name:
        if user_id not in save_slots:
            save_slots[user_id] = {}
        session_data = session.get("active_session")
        if session_data:
            save_slots[user_id][slot_name] = session_data
    return redirect(url_for("save_bp.show_saves"))

@save_bp.route("/load_save/<slot_name>")
def load_save(slot_name):
    user_id = session.get("user")
    if user_id and user_id in save_slots and slot_name in save_slots[user_id]:
        session_data = save_slots[user_id][slot_name]
        new_session = GameSession(user_id)
        new_session.load_from_dict(session_data)

        from app import player_sessions
        player_sessions[user_id] = new_session

        # World logic hook — ensure at least one world triggers chapter
        if new_session.current_world:
            new_session.enter_new_world(new_session.current_world)
    return redirect(url_for("world_scene"))