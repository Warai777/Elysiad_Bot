from flask import Blueprint, request, session, redirect, url_for, render_template
import os, json
from datetime import datetime

save_bp = Blueprint("save_bp", __name__)

SAVE_DIR = "data/saves"
os.makedirs(SAVE_DIR, exist_ok=True)

@save_bp.route("/saves")
def view_saves():
    session_id = session.get("user")
    files = [f for f in os.listdir(SAVE_DIR) if f.startswith(session_id)]
    saves = []
    for f in files:
        with open(os.path.join(SAVE_DIR, f)) as sf:
            data = json.load(sf)
            saves.append({
                "filename": f,
                "description": data.get("description", "No description"),
                "timestamp": data.get("timestamp", "Unknown")
            })
    return render_template("saves.html", saves=saves)

@save_bp.route("/save_manual", methods=["POST"])
def save_manual():
    session_id = session.get("user")
    if not session_id:
        return redirect(url_for("login_page"))

    desc = request.form.get("description", "")
    save_data = {
        "description": desc,
        "timestamp": datetime.utcnow().isoformat(),
        "session": session.get("save_data", {})
    }
    filename = f"{session_id}_{int(datetime.utcnow().timestamp())}.json"
    with open(os.path.join(SAVE_DIR, filename), "w") as f:
        json.dump(save_data, f, indent=2)
    return redirect(url_for("save_bp.view_saves"))