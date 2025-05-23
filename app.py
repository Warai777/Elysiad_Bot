... (truncated unchanged code) ...

@app.route('/world_select')
def world_select():
    with open('data/player_profile.json') as f:
        profile = json.load(f)
    player_tier = profile.get("tier", "10-C")

    if os.path.exists('data/cached_worlds.json'):
        with open('data/cached_worlds.json') as f:
            worlds = json.load(f)
    else:
        worlds = []

    worlds_by_tier = {}
    for w in worlds:
        tier = w.get("tier", "10-C")
        if tier not in worlds_by_tier:
            worlds_by_tier[tier] = []
        worlds_by_tier[tier].append(w)

    return render_template('world_select.html', worlds_by_tier=worlds_by_tier, player_tier=player_tier)

... (rest unchanged) ...