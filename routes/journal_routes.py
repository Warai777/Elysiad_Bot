from flask import Blueprint, session, render_template, redirect, url_for

journal_bp = Blueprint('journal_bp', __name__)

@journal_bp.route('/journal')
def view_journal():
    if 'journal' not in session:
        return redirect(url_for("auth_bp.login"))
    journal = session['journal']
    return render_template('journal.html', journal=journal)
