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
    result["consequence"] = action_entry["consequence"]

    # Load lore data
    with open("data/lore_fragments/lotm_lore.json") as f:
        lore_data = json.load(f)

    unlocked = None
    for key, fragment in lore_data.items():
        if fragment["source"] == action_text:
            lore_trackers[session_id].unlock(key)
            unlocked = fragment
            break

    # World state logic
    if "world_state" in loaded_shard:
        state = loaded_shard["world_state"]
        if result["consequence"] == "gain_clue":
            state["rozel_study_discovered"] = True
        elif result["consequence"] == "trigger_termination":
            state["dorm_unlocked"] = False
        elif result["consequence"] == "reveal_symbol":
            state["cathedral_locked"] = False
        elif result["consequence"] == "gain_oe":
            state["nightwatcher_awareness"] += 10
        result["world_state"] = state

    # Phase progression logic
    current_phase = loaded_shard["main_mission"].get("phase")
    phases = loaded_shard["main_mission"].get("phases", [])
    phase_ids = [p["id"] for p in phases]
    if current_phase in phase_ids:
        idx = phase_ids.index(current_phase)
        if idx + 1 < len(phase_ids):
            loaded_shard["main_mission"]["phase"] = phase_ids[idx + 1]
            result["new_phase"] = phases[idx + 1]

    # Save session state
    result["session"] = player_sessions[session_id].to_dict()
    result["unlocked_lore"] = lore_trackers[session_id].get_all_unlocked()
    result["lore_text"] = unlocked
    result["suspicion_event"] = check_suspicion_thresholds(player_sessions[session_id])
    save_shard_state(session_id, player_sessions[session_id], mission_managers[session_id])

    return jsonify(result)

...TRUNCATED...