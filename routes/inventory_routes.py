from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from app import player_sessions

inventory_bp = Blueprint("inventory_bp", __name__)

@inventory_bp.route("/inventory")
def inventory():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    player = player_sessions[session_id]
    return render_template("inventory.html", items=player.inventory, containers=player.containers, session=player)

@inventory_bp.route("/use_item", methods=["POST"])
def use_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    item_name = request.form.get("item")
    player = player_sessions[session_id]
    item = next((i for i in player.inventory if i["name"] == item_name), None)
    if item:
        player.inventory.remove(item)
        player.log_journal(f"You used the item: {item_name}", type_="system")
        flash(f"You used {item_name}.")
    else:
        flash("Item not found.")
    return redirect(url_for("inventory_bp.inventory"))

@inventory_bp.route("/store_item", methods=["POST"])
def store_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    container_name = request.form.get("container")
    item_name = request.form.get("item")
    player = player_sessions[session_id]
    container = next((c for c in player.containers if c.name == container_name), None)
    if container:
        item = next((i for i in player.inventory if i["name"] == item_name), None)
        if item:
            if container.fits(item):
                container.add_item(item)
                player.inventory.remove(item)
                player.log_journal(f"Stored {item_name} in {container_name}.", type_="system")
                flash(f"Stored {item_name} in {container_name}.")
            else:
                flash("Item does not fit in that container.")
        else:
            flash("Item not found in inventory.")
    else:
        flash("Container not found.")
    return redirect(url_for("inventory_bp.inventory"))