from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint('page', __name__)

@bp.route('/')
def home():
    return render_template('base.html.j2')
