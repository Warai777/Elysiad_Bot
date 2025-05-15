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

    # Generate item (valid or mystery)
    item = generate_item(action_text, player_sessions[session_id])
    if item:
        player_sessions[session_id].inventory.append(item)
        result["item_reward"] = item.get("name")
        player_sessions[session_id].journal.append(f"Acquired item: {item.get('name')}")

    # Attempt to reveal any mystery items
    revealed_items = player_sessions[session_id].reveal_items()
    if revealed_items:
        result["revealed_items"] = revealed_items
        for ri in revealed_items:
            player_sessions[session_id].journal.append(f"You decipher the nature of: {ri}")

    # Save and return
    result["session"] = player_sessions[session_id].to_dict()
    return jsonify(result)

...TRUNCATED...