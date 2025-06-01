from flask import Blueprint, render_template, session, redirect, url_for

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile')
def profile():
    if 'user' not in session or 'profile' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('profile.html', profile=session['profile'])