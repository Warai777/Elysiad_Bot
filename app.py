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

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)