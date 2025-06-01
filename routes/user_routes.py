from flask import Blueprint, render_template, session, redirect, url_for, request
from user_auth import save_player_profile

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session or 'profile' not in session:
        return redirect(url_for('auth_bp.login'))

    profile = session['profile']

    if request.method == 'POST':
        profile['appearance'] = request.form.get('appearance', profile['appearance'])
        profile['speech_style'] = request.form.get('speech_style', profile['speech_style'])
        personality = request.form.get('personality', '')
        profile['personality'] = [p.strip() for p in personality.split(',') if p.strip()]

        save_player_profile(session['user'], profile)
        session['profile'] = profile  # Update session

    return render_template('profile.html', profile=profile)