from flask import Blueprint, render_template, request, redirect, url_for, session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # TEMP: Authenticate everything
        session['user'] = username
        return redirect(url_for('main.choose_world'))  # Adjust to your post-login route
    return render_template('login.html')