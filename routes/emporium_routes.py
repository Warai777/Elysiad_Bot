from flask import Blueprint, render_template
from emporium_generator import generate_emporium_items

emporium_bp = Blueprint('emporium_bp', __name__)

@emporium_bp.route('/emporium')
def emporium():
    items = generate_emporium_items()
    return render_template('emporium.html', items=items)