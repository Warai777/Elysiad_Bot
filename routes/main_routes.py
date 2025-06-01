from flask import Blueprint, session, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('auth_bp.login'))

@main.route('/enter_world')
def enter_world():
    if 'world' not in session or 'entry_mode' not in session:
        return redirect(url_for('main.choose_world'))
    world = session['world']
    mode = session['entry_mode']
    return render_template('world_scene.html', world=world, mode=mode)