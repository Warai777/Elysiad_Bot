...TRUNCATED...

@app.route("/chapters")
def view_chapters():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    chapters = player_sessions[session_id].chapters
    return render_template("chapters.html", chapters=chapters)

...TRUNCATED...