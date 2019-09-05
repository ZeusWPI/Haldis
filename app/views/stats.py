from flask import Blueprint
from flask import current_app as app
from flask import render_template

from fatmodels import FatLocation, FatOrder, FatOrderItem, FatProduct, FatUser

stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/")
def stats():
    data = {
        "amount": {
            "orders": FatOrder.amount(),
            "locations": FatLocation.amount(),
            "users": FatUser.amount(),
            "orderitems": FatOrderItem.amount(),
            "products": FatProduct.amount(),
        }
    }
    return render_template("stats.html", data=data)
