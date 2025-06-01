from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['user'] = username  # TEMP: Authenticate all
        return redirect(url_for('main.choose_world'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # TEMP: Accept all new users
        session['user'] = username
        return redirect(url_for('main.choose_world'))
    return render_template('signup_page.html')