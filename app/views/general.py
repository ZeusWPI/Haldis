import os
from datetime import datetime, timedelta

from flask import Blueprint, abort
from flask import current_app as app
from flask import render_template, send_from_directory, url_for
from flask_login import login_required

from models import Location, Order

# import views
from views.order import get_orders

general_bp = Blueprint("general_bp", __name__)


@general_bp.route("/")
def home():
    prev_day = datetime.now() - timedelta(days=1)
    recently_closed = get_orders(
        ((Order.stoptime > prev_day) & (Order.stoptime < datetime.now()))
    )
    return render_template(
        "home.html", orders=get_orders(), recently_closed=recently_closed
    )


@general_bp.route("/map", defaults={"id": None})
@general_bp.route("/map/<int:id>")
def map(id):
    locs = Location.query.order_by("name")
    return render_template("maps.html", locations=locs)


@general_bp.route("/location")
def locations():
    locs = Location.query.order_by("name")
    return render_template("locations.html", locations=locs)


@general_bp.route("/location/<int:id>")
def location(id):
    loc = Location.query.filter(Location.id == id).first()
    if loc is None:
        abort(404)
    return render_template("location.html", location=loc, title=loc.name)


@general_bp.route("/about/")
def about():
    return render_template("about.html")


@general_bp.route("/profile/")
@login_required
def profile():
    return render_template("profile.html")


@general_bp.route("/favicon.ico")
def favicon():
    if len(get_orders((Order.stoptime > datetime.now()))) == 0:
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/x-icon",
        )
    else:
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon_orange.ico",
            mimetype="image/x-icon",
        )
