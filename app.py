...TRUNCATED...

@app.route("/export_journal")
def export_journal():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))

    import json
    from flask import Response
    journal_data = player_sessions[session_id].journal
    json_data = json.dumps(journal_data, indent=2)
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=journal_export.json"}
    )

...TRUNCATED...