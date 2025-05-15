...TRUNCATED...

@app.route("/add_journal_entry", methods=["POST"])
def add_journal_entry():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    note = request.form.get("note", "").strip()
    if note:
        player_sessions[session_id].log_custom_note(note)
    return redirect(url_for("view_journal"))

...TRUNCATED...