...TRUNCATED...

@app.route("/world_scene")
def world_scene():
    global loaded_shard
    if not loaded_shard:
        with open("data/shards/lotm_demo_shard.json") as f:
            loaded_shard = json.load(f)

    current_phase = loaded_shard["main_mission"].get("phase")
    filtered_actions = [a for a in loaded_shard["actions"] if current_phase in a.get("phases", [])]
    return render_template("world_scene.html", shard=loaded_shard, actions=filtered_actions)

...TRUNCATED...