from flask import Blueprint, session, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('auth_bp.login'))

@main.route('/choose-world')
def choose_world():
    player = session.get('profile')
    return render_template('library.html', player=player)

@main.route('/enter_world')
def enter_world():
    if 'world' not in session or 'entry_mode' not in session:
        return redirect(url_for('main.choose_world'))
    world = session['world']
    mode = session['entry_mode']

    if session.get('phase') == 'ResetRequired':
        return redirect(url_for('main.death_screen'))

    return render_template('world_scene.html', world=world, mode=mode)

@main.route('/death')
def death_screen():
    session.pop('journal', None)
    session['suspicion'] = 0
    session['phase'] = "Intro"
    return render_template('death_screen.html')