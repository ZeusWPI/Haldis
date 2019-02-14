from datetime import datetime, timedelta

from flask import url_for, render_template, abort
from flask_login import login_required

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


@app.route('/map', defaults= {'id': None})
@app.route('/map/<int:id>')
def map(id):
    locs = Location.query.order_by('name') 
    return render_template('maps.html', locations= locs)  


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
