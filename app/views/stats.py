"Script to generate the stats related views of Haldis"
from flask import Blueprint
from flask import current_app as app
from flask import render_template

from fatmodels import FatLocation, FatOrder, FatOrderItem, FatUser

stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/")
def stats() -> str:
    "Generate Haldis data in a pretty format"
    data = {
        "amount": {
            "orders": FatOrder.amount(),
            "locations": FatLocation.amount(),
            "users": FatUser.amount(),
            "orderitems": FatOrderItem.amount(),
        }
    }
    return render_template("stats.html", data=data)
