from flask import Blueprint, session, redirect, url_for, render_template, request, Response
import json
from globals import player_sessions

journal_bp = Blueprint("journal_bp", __name__)

@journal_bp.route("/journal")
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

@journal_bp.route("/add_journal_entry", methods=["POST"])
def add_journal_entry():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    note = request.form.get("note", "").strip()
    if note:
        player_sessions[session_id].log_custom_note(note)
    return redirect(url_for("journal_bp.view_journal"))

@journal_bp.route("/export_journal")
def export_journal():
    session_id = session.get("user")
    if not session_id or session_id not in player_sessions:
        return redirect(url_for("login_page"))
    journal_data = player_sessions[session_id].journal
    json_data = json.dumps(journal_data, indent=2)
    return Response(json_data, mimetype="application/json", headers={"Content-Disposition": "attachment;filename=journal_export.json"})