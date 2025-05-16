...TRUNCATED...

@app.route("/world_scene", methods=["GET", "POST"])
def world_scene():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    current_session = player_sessions[session_id]
    current_session.autosave_if_needed()
    story_text = ""
    if request.method == "POST":
        from story_manager import generate_story_scene
        story_text = generate_story_scene(current_session)
    return render_template("world_scene.html", session=current_session, story_text=story_text)

...TRUNCATED...