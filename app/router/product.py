from flask import Blueprint
from flask import request
from flask import jsonify, abort
from flask_jwt_extended import *

import json

from app.jwt_middleware import is_admin
from model import product
from app.db import get_oracle


bp = Blueprint("product", __name__, url_prefix="/product")

def table_converter(rows):
    pdts = []
    for row in rows:
        pdt = product.Product(row)
        pdts.append(json.loads(pdt.to_json()))

    return pdts


@bp.route("/", methods=["GET"])
@jwt_required()
def get_product():
    db = get_oracle()
    cursor = db.cursor()

    parameter_dict = request.args.to_dict()

    key = parameter_dict['opt']
    value = parameter_dict['value']

    query = f"select * from product where {key} = \'{value}\'"
    try:
        rows = cursor.execute(query)
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )

    return table_converter(rows)


@bp.route("/used", methods=["GET"])
@jwt_required()
def get_product_used():
    db = get_oracle()
    cursor = db.cursor()

    query = f"select * from product where name like \'%USED\'"
    rows = cursor.execute(query)

    return table_converter(rows)


@bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_product():
    db = get_oracle()
    cursor = db.cursor()
    query = "select * from product"

    rows = cursor.execute(query)

    return table_converter(rows)


@bp.route("/totals_by", methods=["GET"])
@jwt_required() # Only Admin
def get_product_group_count():
    if not is_admin():
        return abort(403, description="You are not admin")

    db = get_oracle()
    cursor = db.cursor()

    parameter_dict = request.args.to_dict()
    col = parameter_dict['col']

    query = f"select {col}, count(*) from product group by {col}"
    rows = cursor.execute(query)

    ret = []
    for row in rows:
        res = {"vendor": row[0], "count": row[1]}
        ret.append(res)
    return ret


@bp.route("/", methods=["PUT"])
@jwt_required() # Only Admin
def update_product():
    if not is_admin():
        return abort(403, description="You are not admin")

    db = get_oracle()
    cursor = db.cursor()

    parameter_dict = request.args.to_dict()
    key = parameter_dict['opt']
    value = parameter_dict['value']

    params = request.get_json()
    new_pdt = product.Product(params.values())

    query = f"update product " \
            f"set " \
            f"name=\'{new_pdt.name}\', " \
            f"price=\'{new_pdt.price}\', " \
            f"category=\'{new_pdt.category}\', " \
            f"vendor=\'{new_pdt.category}\' " \
            f"where {key} = \'{value}\'"

    try:
        cursor.execute(query)
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        db.commit()
        return jsonify(
            success=True
        )


@bp.route("/", methods=["DELETE"])
@jwt_required() # Only Admin
def delete_product():
    if not is_admin():
        return abort(403, description="You are not admin")

    db = get_oracle()
    cursor = db.cursor()

    parameter_dict = request.args.to_dict()
    key = parameter_dict['opt']
    value = parameter_dict['value']

    query = f"delete from product where {key} = \'{value}\'"
    try:
        cursor.execute(query)
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        db.commit()
        return jsonify(
            success=True
        )
