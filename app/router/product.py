from flask import Blueprint
from flask import request
from flask import jsonify, abort
from flask_jwt_extended import *
from app.jwt_middleware import is_admin

import json
from sqlalchemy import func

from model.product import Product
from app.db import sql

bp = Blueprint("product", __name__, url_prefix="/product")

json_converter = lambda x: json.loads(x.json)
def table_converter(rows):
     pdts = [json_converter(x) for x in rows]
     return pdts


@bp.route("/", methods=["GET"])
@jwt_required()
def get_product():
    parameter_dict = request.args.to_dict()

    key = parameter_dict['opt']
    value = parameter_dict['value']
    query_filter = {key: value}

    pdts = Product.query.filter_by(**query_filter).all()
    return table_converter(pdts)


@bp.route("/used", methods=["GET"])
@jwt_required()
def get_product_used():
    pdts = Product.query.filter(Product.name.like("%USED")).all()
    return table_converter(pdts)


@bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_product():
    pdts = Product.query.all()
    return table_converter(pdts)


@bp.route("/totals_by", methods=["GET"])
@jwt_required() # Only Admin
def get_product_group_count():
    if not is_admin():
        return abort(403, description="You are not admin")

    parameter_dict = request.args.to_dict()
    column = parameter_dict['col']

    pdts = None
    if column == "vendor":
        pdts = sql.session.query(
            Product.vendor,
            func.count("*").
            label("total_counts")).\
            group_by(Product.vendor).\
            all()
    elif column == "category":
        pdts = sql.session.query(
            Product.category,
            func.count("*").
            label("total_counts")). \
            group_by(Product.category). \
            all()

    ret = []
    for row in pdts:
        res = {column: row[0], "count": row[1]}
        ret.append(res)

    return ret


@bp.route("/", methods=["PUT"])
@jwt_required() # Only Admin
def update_product():
    if not is_admin():
        return abort(403, description="You are not admin")
    parameter_dict = request.args.to_dict()

    key = parameter_dict['opt']
    value = parameter_dict['value']

    req_json = request.get_json()

    try:
        if key == "seq":
            sql.session.query(Product).filter(Product.seq == value).update(req_json)
        elif key == "name":
            sql.session.query(Product).filter(Product.name == value).update(req_json)
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        sql.session.commit()
        return jsonify(
            success=True
        )


@bp.route("/", methods=["DELETE"])
@jwt_required() # Only Admin
def delete_product():
    if not is_admin():
        return abort(403, description="You are not admin")

    parameter_dict = request.args.to_dict()

    key = parameter_dict['opt']
    value = parameter_dict['value']

    del_pdt: Product | None = None
    try:
        if key == "seq":
            del_pdt = sql.session.query(Product).filter(Product.seq == value).first()
        elif key == "name":
            del_pdt = sql.session.query(Product).filter(Product.name == value).first()
    except Exception as e:
        error = e
        return jsonify(
            success=False,
            error=error
        )
    else:
        sql.session.delete(del_pdt)
        sql.session.commit()
        return jsonify(
            success=True
        )
