...TRUNCATED...

@app.route("/inventory")
def inventory():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    items = player_sessions[session_id].inventory
    return render_template("inventory.html", items=items)

...TRUNCATED...