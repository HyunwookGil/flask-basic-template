from flask import Blueprint
from flask import request
from flask_jwt_extended import *

from app.db import get_oracle, get_mysql, get_mongo


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/vendor_total", methods=["GET"])
@jwt_required()
def get_user_vendor_total():
    oracle = get_oracle()
    oracle_cursor = oracle.cursor()
    mysql = get_mysql()
    mysql_cursor = mysql.cursor()
    mongo = get_mongo()
    coll = mongo["Order"]["order"]

    parameter_dict = request.args.to_dict()
    user_seq = parameter_dict["seq"]

    # Find user id
    mysql_query = f"select id from User where seq={user_seq}"
    mysql_cursor.execute(mysql_query)
    user_id = mysql_cursor.fetchone()[0]

    # Set Vendors
    vendors = dict()
    totals = dict()
    oracle_query = f"select * from vendor"
    rows = oracle_cursor.execute(oracle_query)
    for row in rows:
        seq, vendor = row
        vendors[seq] = vendor
        totals[seq] = 0

    # Set Products
    prds = dict()
    oracle_query = f"select seq, vendor from product"
    rows = oracle_cursor.execute(oracle_query)
    for row in rows:
        seq, vendor = row
        prds[seq] = vendor

    # make tally by production_id
    mongo_filter = {'buyer_id': int(user_seq)}
    docs = coll.find(mongo_filter)
    for doc in docs:
        for prd_order in doc["product_orders"]:
            totals[prds[prd_order["product_id"]]] += prd_order["price"]

    vendors_total = dict()
    for key, value in vendors.items():
        vendors_total[value] = totals[key]
    vendors_total.update({"user": user_id})

    return vendors_total