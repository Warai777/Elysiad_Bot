from flask import Flask, render_template, redirect, request, session, url_for
from flask_cors import CORS
from routes.journal_routes import journal_bp
from routes.user_routes import user_bp
from routes.character_routes import character_bp
from routes.auth_routes import auth_bp
from routes.emporium_routes import emporium_bp
from routes.chapter_routes import chapter_bp
import os

# App init
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev")

# Register blueprints
app.register_blueprint(journal_bp)
app.register_blueprint(user_bp)
app.register_blueprint(character_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(emporium_bp)
app.register_blueprint(chapter_bp)

# Routes
@app.route('/')
def index():
    return redirect(url_for('auth_bp.login'))

if __name__ == '__main__':
    app.run(debug=True)