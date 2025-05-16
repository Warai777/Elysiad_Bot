from flask import Blueprint, render_template, request, redirect, url_for, session
from globals import player_sessions

inventory_bp = Blueprint("inventory_bp", __name__)

@inventory_bp.route("/inventory")
def inventory():
    sid = session.get("user")
    if not sid or sid not in player_sessions:
        return redirect(url_for("login_page"))

    ps = player_sessions[sid]
    return render_template("inventory.html", items=ps.inventory, containers=ps.containers, session=ps)