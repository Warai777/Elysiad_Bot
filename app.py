...TRUNCATED...

@app.route("/submit_action", methods=["POST"])
def submit_action():
    session_id = session.get("user")
    data = request.get_json()
    action_text = data.get("action")

    if not session_id or session_id not in player_sessions:
        return jsonify({"error": "No active session"}), 400

    # Look up action type and consequence from shard
    action_entry = next((a for a in loaded_shard["actions"] if a["text"] == action_text), None)
    if not action_entry:
        action_entry = {"type": "random", "consequence": "none"}

    handler = ActionHandler(player_sessions[session_id])
    result = handler.handle_action(action_text, action_type=action_entry["type"])

    # Add consequence to result
    result["consequence"] = action_entry["consequence"]

    # Update lore if critical success
    if result['outcome'] == 'critical_success':
        lore_trackers[session_id].unlock(f"lore_{len(lore_trackers[session_id].unlocked_fragments)+1}")

    # Check suspicion events
    result["suspicion_event"] = check_suspicion_thresholds(player_sessions[session_id])

    # Save progress
    save_shard_state(session_id, player_sessions[session_id], mission_managers[session_id])

    result["session"] = player_sessions[session_id].to_dict()
    result["unlocked_lore"] = lore_trackers[session_id].get_all_unlocked()
    return jsonify(result)

...TRUNCATED...