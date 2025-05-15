...TRUNCATED...

@app.route("/store_item", methods=["POST"])
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
                player.journal.append(f"Stored {item_name} in {container_name}.")
                flash(f"Stored {item_name} in {container_name}.")
            else:
                flash("Item does not fit in that container.")
        else:
            flash("Item not found in inventory.")
    else:
        flash("Container not found.")

    return redirect(url_for("inventory"))

...TRUNCATED...