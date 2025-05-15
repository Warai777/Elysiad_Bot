...TRUNCATED...

@app.route("/journal")
def view_journal():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    filter_type = request.args.get("type", "")
    keyword = request.args.get("keyword", "")
    entries = player_sessions[session_id].journal

    if filter_type:
        entries = [e for e in entries if e.get("type") == filter_type]
    if keyword:
        entries = [e for e in entries if keyword.lower() in e.get("text", "").lower()]

    entries = entries[-100:][::-1]
    return render_template("journal.html", entries=entries, filter_type=filter_type, keyword=keyword)

...TRUNCATED...