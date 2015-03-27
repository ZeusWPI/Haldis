from flask import url_for, render_template, abort
from flask.ext.login import current_user
from datetime import datetime

from app import app
from models import Order



@app.route('/')
def home():
   if not current_user.is_anonymous():
        orders = Order.query.filter(Order.stoptime > datetime.now()).all()
        return render_template('home_loggedin.html', orders=orders)
   return render_template('home.html')


@app.route('/about/')
def about():
   return render_template('about.html')


@app.route('/stats/')
def stats():
   return render_template('stats.html')


@app.route('/order/<int:id>')
def order(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        return render_template('order.html', order=order)
    return abort(404)

if app.debug:  # add route information
    @app.route('/routes')
    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote(
                "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        string = ''
        for line in sorted(output):
            string += line + "<br/>"

        return string
