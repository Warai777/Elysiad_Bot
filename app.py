from flask import Flask, render_template
from flask_cors import CORS
from user_auth import auth_bp
from routes.journal_routes import journal_bp
from routes.world_routes import world_bp
from routes.story_routes import story_bp
from routes.companion_routes import companion_bp
from routes.choice_routes import choice_bp
from routes.character_routes import character_bp
from routes.emporium_routes import emporium_bp
from routes.chapter_routes import chapter_bp
from routes.entry_routes import entry_bp
from session_store import player_sessions

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(world_bp)
app.register_blueprint(story_bp)
app.register_blueprint(companion_bp)
app.register_blueprint(choice_bp)
app.register_blueprint(character_bp)
app.register_blueprint(emporium_bp)
app.register_blueprint(chapter_bp)
app.register_blueprint(entry_bp)

# Root route for testing
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)