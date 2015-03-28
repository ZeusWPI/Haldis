__author__ = 'feliciaan'

from flask import url_for, render_template, abort, redirect, request
from flask.ext.login import current_user, login_required
from datetime import datetime

from app import app, db
from models import Order, OrderItem

# import views
import views.order

@app.route('/')
def home():
    return render_template('home.html', orders=views.order.get_orders())


@app.route('/about/')
def about():
   return render_template('about.html')


@app.route('/stats/')
def stats():
   return render_template('stats.html')


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
