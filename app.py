...TRUNCATED...

@app.route("/journal_dynamic")
def journal_dynamic():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    return render_template("journal_dynamic.html", journal=player_sessions[session_id].journal)

...TRUNCATED...