from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('create_character'))

@app.route('/create_character')
def create_character():
    return render_template('create_character.html')

@app.route('/save_character', methods=['POST'])
def save_character():
    profile = {
        "name": request.form['name'],
        "appearance": request.form['appearance'],
        "personality": [trait.strip() for trait in request.form['personality'].split(',')],
        "speech_style": request.form['speech_style'],
        "origin_essence": 0,
        "worlds_visited": [],
        "suspicion_level": 0
    }
    with open('data/player_profile.json', 'w') as f:
        json.dump(profile, f, indent=2)
    return redirect(url_for('select_entry_mode'))

@app.route('/select_entry_mode')
def select_entry_mode():
    return render_template('entry_mode_select.html')

@app.route('/enter_world', methods=['POST'])
def enter_world():
    mode = request.form['mode']
    if mode == 'canon':
        character = {
            "name": "Shinji Ikari",
            "source_work": "Neon Genesis Evangelion",
            "expected_arc": "A reluctant pilot who hesitates, breaks under pressure, and struggles with isolation and fear.",
            "intro": "You are Shinji Ikari. The city trembles under the shadow of a descending angel. The phone in your hand won't ring fast enough. The machine that awaits you isn't just a weapon — it's a mirror."
        }
        return render_template('canon_intro.html', character=character)
    elif mode == 'original':
        with open('data/player_profile.json') as f:
            profile = json.load(f)
        return render_template('original_intro.html', profile=profile)
    else:
        return "Invalid mode selected."

if __name__ == '__main__':
    app.run(debug=True)