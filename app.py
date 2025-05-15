...TRUNCATED...

@app.route("/journal")
def view_journal():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    entries = player_sessions[session_id].journal[-100:][::-1]  # most recent first
    return render_template("journal.html", entries=entries)

...TRUNCATED...