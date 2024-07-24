"Script to generate the general views of Haldis"
import json
import os
from datetime import datetime, timedelta
from typing import Optional

import yaml
from flask import Blueprint, Flask, abort
from flask import current_app as app
from flask import (
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from ..hlds.definitions import location_definitions, time_sorted_locations
from ..hlds.models import Location
from ..models import Order
from ..utils import first

# import views
from ..views.order import get_orders

general_bp = Blueprint("general_bp", __name__)


with open(os.path.join(os.path.dirname(__file__), "themes.yml")) as _stream:
    _theme_data = yaml.safe_load(_stream)
    THEME_OPTIONS = _theme_data["options"]
    THEMES = _theme_data["themes"]


@general_bp.route("/")
def home() -> str:
    "Generate the home view"
    prev_day = datetime.now() - timedelta(days=1)
    recently_closed = get_orders(
        (Order.stoptime > prev_day) & (Order.stoptime < datetime.now())
    )
    return render_template(
        "home.html",
        orders=get_orders(
            (
                (datetime.now() > Order.starttime) & (Order.stoptime > datetime.now())
                | (Order.stoptime == None)
            )
        ),
        recently_closed=recently_closed,
    )


def is_theme_active(theme, now):
    theme_type = theme["type"]

    if theme_type == "static":
        return True

    if theme_type == "seasonal":
        start_day, start_month = map(int, theme["start"].split("/"))
        start_datetime = datetime(year=now.year, day=start_day, month=start_month)

        end_day, end_month = map(int, theme["end"].split("/"))
        end_year = now.year + (1 if start_month > end_month else 0)
        end_datetime = datetime(year=end_year, day=end_day, month=end_month)

        return start_datetime <= now <= end_datetime

    raise Exception(f"Unknown theme type {theme_type}")


def get_theme_css(theme, options):
    # Build filename
    # Each option's chosen value is appended, to get something like mytheme_darkmode_heavy.css

    filename = theme["file"]

    for option in theme.get("options", []):
        theme_name = theme["name"]
        assert (
            option in THEME_OPTIONS
        ), f"Theme `{theme_name}` uses undefined option `{option}`"

        chosen_value = options[option]
        possible_values = list(THEME_OPTIONS[option].keys())

        value = (
            chosen_value
            if chosen_value in possible_values
            else THEME_OPTIONS[option]["_default"]
        )

        filename += "_" + value

    filename += ".css"

    theme_css_dir = "static/css/themes/"
    return os.path.join(app.root_path, theme_css_dir, filename)


def get_active_themes():
    now = datetime.now()
    return [theme for theme in THEMES if is_theme_active(theme, now)]


@general_bp.route("/theme.css")
def theme_css():
    "Send appropriate CSS for current theme"
    themes = get_active_themes()

    theme_name = request.cookies.get("theme", None)
    theme = first((t for t in themes if t["file"] == theme_name), default=themes[-1])

    options = {
        name: request.cookies.get("theme_" + name, None)
        for name in ["atmosphere", "performance"]
    }

    path = get_theme_css(theme, options)

    with open(path) as f:
        response = make_response(f.read())
    response.headers["Content-Type"] = "text/css"

    return response


@general_bp.route("/current_theme.js")
def current_theme_js():
    themes = get_active_themes()

    selected_theme_name = request.cookies.get("theme", None)
    matching_theme = first(t for t in themes if t["file"] == selected_theme_name)
    cur_theme = matching_theme or themes[-1]

    response = make_response(
        rf"""
var currentTheme        = {json.dumps(cur_theme['file'])};
var currentThemeOptions = {json.dumps(cur_theme.get('options', []))};
"""
    )
    response.headers["Content-Type"] = "text/javascript"

    # Theme name that is not valid at this moment: delete cookie
    if matching_theme is None:
        response.delete_cookie("theme", path="/")

    return response


@general_bp.route("/map")
def map_view() -> str:
    "Generate the map view"
    return render_template("maps.html", locations=location_definitions)


@general_bp.route("/location")
def locations() -> str:
    "Generate the location view"
    return render_template("locations.html", locations=time_sorted_locations())


@general_bp.route("/location/<location_id>")
def location(location_id) -> str:
    "Generate the location view given an id"
    loc = first(filter(lambda l: l.id == location_id, location_definitions))
    if loc is None:
        abort(404)
    return render_template("location.html", location=loc, title=loc.name)


@general_bp.route("/location/<location_id>/<dish_id>")
def location_dish(location_id, dish_id) -> str:
    loc: Optional[Location] = first(
        filter(lambda l: l.id == location_id, location_definitions)
    )
    if loc is None:
        abort(404)
    dish = loc.dish_by_id(dish_id)
    if dish is None:
        abort(404)
    return jsonify(
        [
            {
                "type": c[0],
                "id": c[1].id,
                "name": c[1].name,
                "description": c[1].description,
                "options": [
                    {
                        "id": o.id,
                        "name": o.name,
                        "description": o.description,
                        "price": o.price,
                        "tags": o.tags,
                    }
                    for o in c[1].options
                ],
            }
            for c in dish.choices
        ]
    )


@general_bp.route("/about/")
def about() -> str:
    "Generate the about view"
    return render_template("about.html")


@general_bp.route("/profile/")
@login_required
def profile() -> str:
    "Generate the profile view"
    return render_template("profile.html", themes_list=get_active_themes())


@general_bp.route("/favicon.ico")
def favicon() -> str:
    "Generate the favicon"
    # pylint: disable=R1705
    if not get_orders(Order.stoptime > datetime.now()):
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
