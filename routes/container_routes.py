from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from app import player_sessions

container_bp = Blueprint("container_bp", __name__)

@container_bp.route("/containers")
def containers():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    player = player_sessions[session_id]
    return render_template("containers.html", containers=player.containers)

@container_bp.route("/transfer_item", methods=["POST"])
def transfer_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    container_name = request.form.get("container")
    item_name = request.form.get("item")
    player = player_sessions[session_id]
    container = next((c for c in player.containers if c.name == container_name), None)

    if container:
        item = next((i for i in container.items if i["name"] == item_name), None)
        if item:
            if player.can_carry(item.get("weight", 0)):
                if container.remove_item(item_name):
                    player.inventory.append(item)
                    player.log_journal(f"Transferred {item_name} from {container_name} to main inventory.", type_="system")
                    flash(f"You transferred {item_name} to your inventory.")
                else:
                    flash("Failed to remove item from container.")
            else:
                flash("You cannot carry that much weight.")
        else:
            flash("Item not found in container.")
    else:
        flash("Container not found.")
    return redirect(url_for("container_bp.containers"))