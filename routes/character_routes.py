from flask import Blueprint

character_bp = Blueprint('character_bp', __name__)

# Placeholder route
@character_bp.route('/character')
def character_home():
    return "Character route placeholder."