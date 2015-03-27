__author__ = 'feliciaan'
from flask import url_for, render_template, abort, redirect
from flask.ext.login import current_user, login_required
from datetime import datetime

from app import app, db
from models import Order, OrderItem
from forms import OrderItemForm, OrderForm


@app.route('/order/<id>')
@login_required
def order(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        return render_template('order.html', order=order)
    return abort(404)


@app.route('/order/<id>/create', methods=['GET', 'POST'])
@login_required
def order_item_create(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        form = OrderItemForm()
        form.populate(order.location)
        if form.validate_on_submit():
            item = OrderItem()
            form.populate_obj(item)
            item.order_id = id
            item.user_id = current_user.id
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('order', id=id))
        return render_template('order_form.html', form=form, url=url_for("order_item_create", id=id))
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

    return render_template('order_form.html', form=orderForm, url=url_for("order_create"))


@app.route('/order')
@login_required
def orders():
    orders = Order.query.filter((Order.stoptime > datetime.now()) | (Order.stoptime == None)).all()
    orderForm = OrderForm()
    orderForm.populate()
    return render_template('orders.html', orders=orders, form=orderForm)

