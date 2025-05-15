...TRUNCATED...

@app.route("/containers")
def containers():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    return render_template("containers.html", containers=player_sessions[session_id].containers)

...TRUNCATED...