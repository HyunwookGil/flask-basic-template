from flask import Blueprint
from flask import request
from flask import jsonify, abort
from flask_jwt_extended import *
from app.jwt_middleware import is_admin

from model.order import Order


bp = Blueprint("order", __name__, url_prefix="/order")


@bp.route("/", methods=["GET"])
@jwt_required()
def get_order():
    parameter_dict = request.args.to_dict()
    opt = parameter_dict["opt"]
    val = parameter_dict["value"]

    query_filter = {opt: val}

    orders = Order.objects(**query_filter)
    return jsonify(orders)


@bp.route("/", methods=["POST"])
@jwt_required() # Only Admin
def new_order():
    if not is_admin():
        return abort(403, description="You are not admin")

    global ord

    req_json = request.get_json()

    try:
        ord = Order(**req_json)

        ord.issue_order_id()
        ord.re_tally()
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        ord.save()
        return jsonify(
            success=True,
            order=ord
        )


@bp.route("/", methods=["PUT"])
@jwt_required() # Only Admin
def update_order():
    if not is_admin():
        return abort(403, description="You are not admin")

    req_json = request.get_json()

    parameter_dict = request.args.to_dict()
    query_filter = {"order_id": parameter_dict["order_id"]}

    try:
        Order.objects.get_or_404(**query_filter).update(**req_json)
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        ord = Order.objects(**query_filter).first()
        return jsonify(
            success=True,
            order=ord
        )
