__author__ = 'feliciaan'
from flask import url_for, render_template, abort, redirect, Blueprint, flash
from flask.ext.login import current_user, login_required
from datetime import datetime

from app import app, db
from models import Order, OrderItem
from forms import OrderItemForm, OrderForm

order_bp = Blueprint('order_bp', 'order')

@order_bp.route('/')
@login_required
def orders():
    orders = Order.query.filter((Order.stoptime > datetime.now()) | (Order.stoptime == None)).all()
    orderForm = OrderForm()
    orderForm.populate()
    return render_template('orders.html', orders=orders, form=orderForm)


@order_bp.route('/create', methods=['GET', 'POST'])
@login_required
def order_create():
    orderForm = OrderForm()
    orderForm.populate()
    if orderForm.validate_on_submit():
        order = Order()
        orderForm.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('.order', id=order.id))

    return render_template('order_form.html', form=orderForm, url=url_for(".order_create"))


@order_bp.route('/<id>')
@login_required
def order(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        form = OrderItemForm()
        form.populate(order.location)
        total_price = sum([o.food.price for o in order.orders])
        return render_template('order.html', order=order, form=form, total_price=total_price)
    return abort(404)


@order_bp.route('/<id>/create', methods=['GET', 'POST'])
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
            return redirect(url_for('.order', id=id))
        return render_template('order_form.html', form=form, url=url_for(".order_item_create", id=id))
    return abort(404)

@order_bp.route('/<order_id>/<item_id>/delete')
@login_required
def delete_item(order_id, item_id):
    item = OrderItem.query.filter(OrderItem.id == item_id).first()
    if item.can_delete(order_id, current_user.id):
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('.order', id=order_id))
    abort(404)


@order_bp.route('/<id>/volunteer')
@login_required
def volunteer(id):
    order = Order.query.filter(Order.id == id).first()
    if order is not None:
        print(order.courrier_id)
        if order.courrier_id == 0:
            order.courrier_id = current_user.id
            db.session.commit()
            flash("Thank you for volunteering!")
        else:
            flash("Volunteering not possible!")
        return redirect(url_for('.order', id=id))
    abort(404)

app.register_blueprint(order_bp, url_prefix='/order')