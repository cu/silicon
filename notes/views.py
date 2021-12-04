from flask import (
    Blueprint,
)

bp = Blueprint('page', __name__)

@bp.route('/')
def home():
    return "it works"
