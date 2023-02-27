from flask import (
    Blueprint, jsonify
)

from app.db import get_mysql, get_oracle, get_mongo

bp = Blueprint('landing', __name__)


# index page
@bp.route('/')
def index():
    return jsonify(
        ret="Hello flask"
    )
