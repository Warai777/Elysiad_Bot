from flask import Blueprint, render_template

chapter_bp = Blueprint('chapter_bp', __name__)

@chapter_bp.route('/chapters')
def chapter_list():
    return render_template('chapters.html')  # Basic placeholder