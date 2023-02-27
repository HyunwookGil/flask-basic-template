from flask import Blueprint
from flask import request
from flask_jwt_extended import *

from model.user import User
from model.product import Product
from model.order import Order
from model.vendor import Vendor


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/vendor_total", methods=["GET"])
@jwt_required()
def get_user_vendor_total():
    parameter_dict = request.args.to_dict()
    user_seq = parameter_dict["seq"]

    # Find user id
    query_filter = {"seq": user_seq}
    user = User.query.filter_by(**query_filter).first()
    user_id = user.id

    # Set Vendors
    vendors = dict()
    totals = dict()
    vds = Vendor.query.all()
    for vd in vds:
        vendors[vd.seq] = vd.name
        totals[vd.seq] = 0

    # Set Products
    products = dict()
    pdts = Product.query.all()
    for pdt in pdts:
        products[pdt.seq] = pdt.vendor

    # make tally by production_id
    query_filter = {'buyer_id': int(user_seq)}
    orders = Order.objects(**query_filter)
    for order in orders:
        for prd_order in order.product_orders:
            totals[products[prd_order.product_id]] += prd_order.price

    vendors_total = dict()
    for key, value in vendors.items():
        vendors_total[value] = totals[key]
    vendors_total.update({"user": user_id})

    return vendors_total