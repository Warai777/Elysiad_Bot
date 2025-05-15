...TRUNCATED...

@app.route("/use_item", methods=["POST"])
def use_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    item = request.form.get("item")
    if item in player_sessions[session_id].inventory:
        player_sessions[session_id].inventory.remove(item)
        player_sessions[session_id].journal.append(f"Used item: {item}")
        flash(f"You used the {item}.")
    else:
        flash("Item not found.")
    return redirect(url_for("inventory"))

...TRUNCATED...