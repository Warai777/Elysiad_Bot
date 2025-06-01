from flask import Blueprint, session, redirect, url_for, request
from world_manager import load_world_data

world_bp = Blueprint('world_bp', __name__)

@world_bp.route('/begin-world', methods=['POST'])
def begin_world():
    world_name = request.form.get('world_name')
    mode = request.form.get('entry_mode')  # 'canon' or 'origin'

    if not world_name or not mode:
        return redirect(url_for('main.choose_world'))

    session['world'] = world_name
    session['entry_mode'] = mode

    # Load and cache world data if needed
    world_data = load_world_data(world_name)
    session['world_data'] = world_data

    return redirect(url_for('main.enter_world'))