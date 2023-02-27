from flask import Blueprint
from flask import request
from flask import jsonify, abort
from flask_jwt_extended import *

import json

from app.jwt_middleware import is_admin
from model import order
from app.db import get_mongo


bp = Blueprint("order", __name__, url_prefix="/order")


def doc_converter(rows):
    ords = []
    for row in rows:
        odr = order.Order.dict_to_cls(row)
        ords.append(json.loads(odr.to_json()))

    return ords


@bp.route("/", methods=["GET"])
@jwt_required()
def get_order():
    mongo = get_mongo()
    coll = mongo["Order"]["order"]

    parameter_dict = request.args.to_dict()
    opt = parameter_dict["opt"]
    val = parameter_dict["value"]

    query = {opt: val}

    try:
        rows = coll.find(query, {"_id": 0}).sort("order_date", -1)
    except Exception as e:
        error=e
        return jsonify(
            success=False,
            error=error
        )
    else:
        return doc_converter(rows)


@bp.route("/", methods=["POST"])
@jwt_required() # Only Admin
def new_order():
    if not is_admin():
        return abort(403, description="You are not admin")

    mongo = get_mongo()
    coll = mongo["Order"]["order"]

    params = request.get_json()

    new_ord = order.Order.dict_to_cls(params)
    new_ord.issue_order_id()
    try:
        coll.insert_one(new_ord.dict(by_alias=True))
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        return jsonify(
            success=True
        )


@bp.route("/", methods=["PUT"])
@jwt_required() # Only Admin
def update_order():
    if not is_admin():
        return abort(403, description="You are not admin")

    mongo = get_mongo()
    coll = mongo["Order"]["order"]

    params = request.get_json()
    parameter_dict = request.args.to_dict()
    order_id = parameter_dict["order_id"]

    update_filter = {'order_id': order_id}
    update_value = {'$set': {params["key"]: params["value"]}}

    try:
        coll.update_one(update_filter, update_value)
        upt_ord = order.Order.dict_to_cls(coll.find_one(update_filter))
        upt_ord.re_tally()

        coll.delete_one(update_filter)
        coll.insert_one(upt_ord.dict(by_alias=True))

    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        return jsonify(
            success=True
        )
