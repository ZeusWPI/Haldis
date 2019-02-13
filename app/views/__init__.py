from datetime import datetime, timedelta

from flask import url_for, render_template, abort, send_from_directory
from flask_login import login_required
import os

from app import app
from models import Order, Location

# import views
from views.order import get_orders
from views import stats


@app.route('/')
def home():
    prev_day = datetime.now() - timedelta(days=1)
    recently_closed = get_orders(
        ((Order.stoptime > prev_day) & (Order.stoptime < datetime.now())))
    return render_template('home.html', orders=get_orders(),
                           recently_closed=recently_closed)


@app.route('/location')
def locations():
    locs = Location.query.order_by('name')
    return render_template('locations.html', locations=locs)


@app.route('/location/<int:id>')
def location(id):
    loc = Location.query.filter(Location.id == id).first()
    if loc is None:
        abort(404)
    return render_template('location.html', location=loc)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/profile/')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/favicon.ico')
def favicon():
    if len(get_orders((Order.stoptime > datetime.now()))) == 0:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')
    else:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon_orange.ico', mimetype='image/x-icon')


if app.debug:  # add route information
    @app.route('/routes')
    @login_required
    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)
            print(rule.endpoint)
            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote(
                "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        string = ''
        for line in sorted(output):
            string += line + "<br/>"

        return string
