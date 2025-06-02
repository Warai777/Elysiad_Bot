from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from user_auth import create_user, validate_user, load_player_profile

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid, message = validate_user(username, password)
        if valid:
            session['user'] = username
            profile = load_player_profile(username)
            if profile:
                session['profile'] = profile
            return redirect(url_for('main.choose_world'))
        else:
            flash(message, 'error')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = create_user(username, password)
        if success:
            session['user'] = username
            profile = load_player_profile(username)
            if profile:
                session['profile'] = profile
            return redirect(url_for('main.choose_world'))
        else:
            flash(message, 'error')
    return render_template('signup_new.html')