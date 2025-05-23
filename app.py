from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from world_templates import generate_ai_world_template
from chapter_saver import load_chapter

app = Flask(__name__)
app.secret_key = 'elysiad_secret_key'

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_path = f'data/users/{username}.json'
        if os.path.exists(user_path):
            with open(user_path) as f:
                user = json.load(f)
            if user['password'] == password:
                session['user'] = username
                return redirect(url_for('create_character'))
        return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_path = f'data/users/{username}.json'
        if os.path.exists(user_path):
            return "Username already exists."
        os.makedirs('data/users', exist_ok=True)
        with open(user_path, 'w') as f:
            json.dump({'username': username, 'password': password}, f, indent=2)
        profile = {
            "name": username,
            "appearance": {},
            "personality": [],
            "speech_style": "",
            "origin_essence": 0,
            "worlds_visited": [],
            "suspicion_level": 0,
            "tier": "10-C"
        }
        with open('data/player_profile.json', 'w') as f:
            json.dump(profile, f, indent=2)
        session['user'] = username
        return redirect(url_for('create_character'))
    return render_template('signup.html')

@app.route('/create_character')
def create_character():
    return render_template('create_character.html')

@app.route('/save_character', methods=['POST'])
def save_character():
    appearance = {
        "hair_color": request.form['hair_color'],
        "eye_color": request.form['eye_color'],
        "skin_color": request.form['skin_color'],
        "height": request.form['height'],
        "build": request.form['build'],
        "style": request.form['style']
    }
    personality_traits = request.form.getlist('personality')
    with open('data/player_profile.json') as f:
        profile = json.load(f)

    profile.update({
        "name": request.form['name'],
        "appearance": appearance,
        "personality": personality_traits,
        "speech_style": request.form['speech_style']
    })

    with open('data/player_profile.json', 'w') as f:
        json.dump(profile, f, indent=2)
    return redirect(url_for('world_entry'))

@app.route('/world_entry')
def world_entry():
    with open('data/player_profile.json') as f:
        player = json.load(f)
    tier = player.get("tier", "10-C")

    if os.path.exists('data/cached_worlds.json'):
        with open('data/cached_worlds.json') as f:
            cached = json.load(f)
    else:
        cached = []

    eligible_worlds = [w for w in cached if w.get("tier") == tier]

    if not eligible_worlds:
        new_world = generate_ai_world_template()
        if new_world['tier'] == tier:
            eligible_worlds.append(new_world)
        with open('data/cached_worlds.json', 'w') as f:
            json.dump([new_world], f, indent=2)

    world = eligible_worlds[-1]
    return render_template('entry_mode_select.html', world=world)

@app.route('/select_entry_mode')
def select_entry_mode():
    return render_template('entry_mode_select.html')

@app.route('/enter_world', methods=['POST'])
def enter_world():
    mode = request.form['mode']
    with open('data/cached_worlds.json') as f:
        world = json.load(f)[-1]

    if mode == 'canon':
        character = world['canon_profile']
        character['source_work'] = world['inspiration']
        return render_template('canon_intro.html', character=character)
    elif mode == 'original':
        with open('data/player_profile.json') as f:
            profile = json.load(f)
        return render_template('original_intro.html', profile=profile)
    else:
        return "Invalid mode selected."

@app.route('/read_chapter/<world>/<int:chapter>')
def read_chapter(world, chapter):
    chapter_data = load_chapter(world, chapter)
    if chapter_data:
        return render_template('chapter_viewer.html', chapter=chapter_data)
    return "Chapter not found."

if __name__ == '__main__':
    app.run(debug=True)