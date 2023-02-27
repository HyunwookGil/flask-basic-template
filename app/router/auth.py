from flask import Blueprint
from flask import flash
from flask import request
from flask import jsonify
from flask_jwt_extended import create_access_token

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.db import get_mysql


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["POST"])
def register():
    params = request.get_json()

    user_id = params["id"]
    passwd = params["passwd"]

    db = get_mysql()
    cursor = db.cursor()
    error = None

    if not user_id:
        error = "user_id is required."
    elif not passwd:
        error = "passwd is required."

    query = "SELECT ID FROM User WHERE ID = %s"
    cursor.execute(query, user_id)
    rows = cursor.fetchone()

    if rows is not None:
        error = f"User {user_id} is already registered."

    if error is None:
        query = "INSERT INTO User (ID, PASSWD) VALUES (%s, %s)"
        cursor.execute(query, (user_id, generate_password_hash(passwd)))
        db.commit()

        flash(error)
        return jsonify(
            success=True
        )

    else:
        return jsonify(
            error=error,
            success=False
        )

@bp.route("/login", methods=["POST"])
def login():
    params = request.get_json()

    user_id = params["id"]
    passwd = params["passwd"]

    db = get_mysql()
    cursor = db.cursor()

    query = "SELECT ID, PASSWD FROM User WHERE ID = %s"
    cursor.execute(query, user_id)

    row = cursor.fetchone()

    error = None
    try:
        db_id, db_passwd = row
    except ValueError:
        error = "ID not exist"
        return jsonify(
            error=error,
            success=False
        )

    if not check_password_hash(db_passwd, passwd):
        error = "Incorrect password."

        return jsonify(
            error=error,
            success=False
        )

    if error is None:
        flash(error)
        return jsonify(
            success=True,
            access_token=create_access_token(identity=user_id,
                                             expires_delta=None)
        )
