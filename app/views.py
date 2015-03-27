from flask import url_for, render_template, abort, redirect, request
from flask.ext.login import current_user, login_required
from datetime import datetime

from app import app, db
from forms import OrderForm
from models import Order



@app.route('/')
def home():
   if not current_user.is_anonymous():
        orders = Order.query.filter((Order.stoptime > datetime.now()) | (Order.stoptime == None)).all()
        return render_template('home_loggedin.html', orders=orders)
   return render_template('home.html')


@app.route('/about/')
def about():
   return render_template('about.html')


@app.route('/stats/')
@login_required
def stats():
   return render_template('stats.html')


@app.route('/order/<int:id>')
@login_required
def order(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        return render_template('order.html', order=order)
    return abort(404)

@app.route('/order/create', methods=['GET', 'POST'])
@login_required
def order_create():
    orderForm = OrderForm()
    orderForm.populate()
    if orderForm.validate_on_submit():
        order = Order()
        orderForm.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('order', id=order.id))

    return render_template('order_form.html', form=orderForm)

@app.route('/order')
@login_required
def orders():
    orders = Order.query.filter((Order.stoptime > datetime.now()) | (Order.stoptime == None)).all()
    orderForm = OrderForm()
    orderForm.populate()
    return render_template('orders.html', orders=orders, form=orderForm)


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

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote(
                "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        string = ''
        for line in sorted(output):
            string += line + "<br/>"

        return string
