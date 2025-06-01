from flask import Blueprint, render_template, session
import os, json

chapter_bp = Blueprint('chapter_bp', __name__)

@chapter_bp.route('/chapters')
def chapter_list():
    player_id = session.get("user")
    chapter_dir = "data/chapters"
    chapters = []

    if player_id:
        for fname in os.listdir(chapter_dir):
            if fname.startswith(f"{player_id}_chapter"):
                with open(os.path.join(chapter_dir, fname)) as f:
                    chapters.append(json.load(f))
        chapters.sort(key=lambda x: x['chapter'])

    return render_template('chapters.html', chapters=chapters)