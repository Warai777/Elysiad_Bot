...TRUNCATED...

@app.route("/transfer_item", methods=["POST"])
def transfer_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    container_name = request.form.get("container")
    item_name = request.form.get("item")

    player = player_sessions[session_id]
    container = next((c for c in player.containers if c["name"] == container_name), None)

    if container:
        item = next((i for i in container["items"] if i["name"] == item_name), None)
        if item:
            total_weight = sum(i.get("weight", 0) for i in player.inventory)
            if total_weight + item.get("weight", 0) <= player.strength * 5:
                container["items"].remove(item)
                player.inventory.append(item)
                player.journal.append(f"Transferred {item_name} from {container_name} to main inventory.")
                flash(f"You transferred {item_name} to your inventory.")
            else:
                flash("You cannot carry that much weight.")
        else:
            flash("Item not found in container.")
    else:
        flash("Container not found.")

    return redirect(url_for("containers"))

...TRUNCATED...