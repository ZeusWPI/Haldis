"Script to generate the general views of Haldis"
import os
from datetime import datetime, timedelta

from flask import Flask, render_template, make_response
from flask import request
from flask import Blueprint, abort
from flask import current_app as app
from flask import render_template, send_from_directory, url_for
from flask_login import login_required

from models import Location, Order
# import views
from views.order import get_orders

general_bp = Blueprint("general_bp", __name__)


@general_bp.route("/")
def home() -> str:
    "Generate the home view"
    prev_day = datetime.now() - timedelta(days=1)
    recently_closed = get_orders(
        ((Order.stoptime > prev_day) & (Order.stoptime < datetime.now()))
    )
    return render_template(
        "home.html", orders=get_orders(), recently_closed=recently_closed
    )

@general_bp.route("/css")
def css():
    "Generate the css"
    if request.cookies.get('theme'):
        if request.cookies['theme'] == 'customTheme':
            #TODO: The custom theme is hardcoded :(. Make the server auto select a custom team.
            f = open("app/static/css/themes/sinterklaas.css")
        else:
            f = open("app/static/css/themes/"+request.cookies['theme']+".css")
    else:
        f = open("app/static/css/main.css")
    response = make_response(f.read())
    response.headers['Content-Type'] = 'text/css'
    return response


@general_bp.route("/map")
def map_view() -> str:
    "Generate the map view"
    locs = Location.query.order_by("name")
    return render_template("maps.html", locations=locs)


@general_bp.route("/location")
def locations() -> str:
    "Generate the location view"
    locs = Location.query.order_by("name")
    return render_template("locations.html", locations=locs)


@general_bp.route("/location/<int:location_id>")
def location(location_id) -> str:
    "Generate the location view given an id"
    loc = Location.query.filter(Location.id == location_id).first()
    if loc is None:
        abort(404)
    return render_template("location.html", location=loc, title=loc.name)


@general_bp.route("/about/")
def about() -> str:
    "Generate the about view"
    return render_template("about.html")


@general_bp.route("/profile/")
@login_required
def profile() -> str:
    "Generate the profile view"
    return render_template("profile.html")


@general_bp.route("/favicon.ico")
def favicon() -> str:
    "Generate the favicon"
    # pylint: disable=R1705
    if not get_orders((Order.stoptime > datetime.now())):
        return send_from_directory(
            os.path.join(str(app.root_path), "static"),
            "favicon.ico",
            mimetype="image/x-icon",
        )
    else:
        return send_from_directory(
            os.path.join(str(app.root_path), "static"),
            "favicon_orange.ico",
            mimetype="image/x-icon",
        )
