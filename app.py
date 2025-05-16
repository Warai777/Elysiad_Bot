...TRUNCATED...

@app.route("/examine_item", methods=["POST"])
def examine_item():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    item_name = request.form.get("item")
    session_data = player_sessions[session_id]
    item = next((i for i in session_data.inventory if i["name"] == item_name and i.get("type") == "mystery"), None)

    if item:
        # Try to trigger reveal
        result = session_data.reveal_items()
        if item_name in result:
            flash(f"You deciphered {item_name}!")
        else:
            flash("You examine it carefully but learn nothing yet.")
    else:
        flash("That item cannot be examined.")
    return redirect(url_for("inventory_bp.inventory"))

...TRUNCATED...