... (existing imports)
from chapter_saver import load_chapter, log_world_entry
... (rest unchanged)

@app.route('/enter_world', methods=['POST'])
def enter_world():
    world_name = request.form.get("world_name")
    mode = request.form.get("mode")

    with open('data/cached_worlds.json') as f:
        cached = json.load(f)

    world = next((w for w in cached if w['name'] == world_name), cached[-1])

    with open('data/player_profile.json') as f:
        profile = json.load(f)

    log_world_entry(world, profile, mode or "preview")

    if mode == 'canon':
        character = world['canon_profile']
        character['source_work'] = world['inspiration']
        return render_template('canon_intro.html', character=character)
    elif mode == 'original':
        return render_template('original_intro.html', profile=profile)
    else:
        return render_template('entry_mode_select.html', world=world)