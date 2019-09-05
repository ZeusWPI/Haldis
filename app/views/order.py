import random
from datetime import datetime

# from flask import current_app as app
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required

from forms import AnonOrderItemForm, OrderForm, OrderItemForm
from models import Order, OrderItem, User, db
from notification import post_order_to_webhook

order_bp = Blueprint("order_bp", "order")


@order_bp.route("/")
def orders(form=None):
    if form is None and not current_user.is_anonymous():
        form = OrderForm()
        location_id = request.args.get("location_id")
        form.location_id.default = location_id
        form.process()
        form.populate()
    return render_template("orders.html", orders=get_orders(), form=form)


@order_bp.route("/create", methods=["POST"])
@login_required
def order_create():
    orderForm = OrderForm()
    orderForm.populate()
    if orderForm.validate_on_submit():
        order = Order()
        orderForm.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        post_order_to_webhook(order)
        return redirect(url_for("order_bp.order", id=order.id))
    return orders(form=orderForm)


@order_bp.route("/<id>")
def order(id, form=None):
    order = Order.query.filter(Order.id == id).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    if form is None:
        form = AnonOrderItemForm() if current_user.is_anonymous() else OrderItemForm()
        form.populate(order.location)
    if order.stoptime and order.stoptime < datetime.now():
        form = None
    total_price = sum([o.product.price for o in order.items])
    debts = sum([o.product.price for o in order.items if not o.paid])
    return render_template(
        "order.html", order=order, form=form, total_price=total_price, debts=debts
    )


@order_bp.route("/<id>/items")
def items_showcase(id, form=None):
    order = Order.query.filter(Order.id == id).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    return render_template("order_items.html", order=order)


@order_bp.route("/<id>/edit", methods=["GET", "POST"])
@login_required
def order_edit(id):
    order = Order.query.filter(Order.id == id).first()
    if current_user.id is not order.courrier_id and not current_user.is_admin():
        abort(401)
    if order is None:
        abort(404)
    orderForm = OrderForm(obj=order)
    orderForm.populate()
    if orderForm.validate_on_submit():
        orderForm.populate_obj(order)
        db.session.commit()
        return redirect(url_for("order_bp.order", id=order.id))
    return render_template("order_edit.html", form=orderForm, order_id=id)


@order_bp.route("/<id>/create", methods=["POST"])
def order_item_create(id):
    current_order = Order.query.filter(Order.id == id).first()
    if current_order is None:
        abort(404)
    if current_order.stoptime and current_order.stoptime < datetime.now():
        abort(404)
    if current_user.is_anonymous() and not current_order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    form = AnonOrderItemForm() if current_user.is_anonymous() else OrderItemForm()
    form.populate(current_order.location)
    if form.validate_on_submit():
        item = OrderItem()
        form.populate_obj(item)
        item.order_id = id
        if not current_user.is_anonymous():
            item.user_id = current_user.id
        else:
            session["anon_name"] = item.name
        db.session.add(item)
        db.session.commit()
        flash("Ordered %s" % (item.product.name), "success")
        return redirect(url_for("order_bp.order", id=id))
    return order(id, form=form)


@order_bp.route("/<order_id>/<item_id>/paid")
@login_required
def item_paid(order_id, item_id):
    item = OrderItem.query.filter(OrderItem.id == item_id).first()
    id = current_user.id
    if item.order.courrier_id == id or current_user.admin:
        item.paid = True
        db.session.commit()
        flash("Paid %s by %s" % (item.product.name, item.get_name()), "success")
        return redirect(url_for("order_bp.order", id=order_id))
    abort(404)


@order_bp.route("/<order_id>/<user_name>/user_paid")
@login_required
def items_user_paid(order_id, user_name):
    user = User.query.filter(User.username == user_name).first()
    items = []
    if user:
        items = OrderItem.query.filter(
            (OrderItem.user_id == user.id) & (OrderItem.order_id == order_id)
        )
    else:
        items = OrderItem.query.filter(
            (OrderItem.name == user_name) & (OrderItem.order_id == order_id)
        )
    current_order = Order.query.filter(Order.id == order_id).first()
    for item in items:
        print(item)
    if current_order.courrier_id == current_user.id or current_user.admin:
        for item in items:
            item.paid = True
        db.session.commit()
        flash("Paid %d items for %s" % (items.count(), item.get_name()), "success")
        return redirect(url_for("order_bp.order", id=order_id))
    abort(404)


@order_bp.route("/<order_id>/<item_id>/delete")
def delete_item(order_id, item_id):
    item = OrderItem.query.filter(OrderItem.id == item_id).first()
    id = None
    if not current_user.is_anonymous():
        print("%s tries to delete orders" % (current_user.username))
        id = current_user.id
    if item.can_delete(order_id, id, session.get("anon_name", "")):
        product_name = item.product.name
        db.session.delete(item)
        db.session.commit()
        flash("Deleted %s" % (product_name), "success")
        return redirect(url_for("order_bp.order", id=order_id))
    abort(404)


@order_bp.route("/<id>/volunteer")
@login_required
def volunteer(id):
    order = Order.query.filter(Order.id == id).first()
    if order is None:
        abort(404)
    if order.courrier_id is None or order.courrier_id == 0:
        order.courrier_id = current_user.id
        db.session.commit()
        flash("Thank you for volunteering!")
    else:
        flash("Volunteering not possible!")
    return redirect(url_for("order_bp.order", id=id))


@order_bp.route("/<id>/close")
@login_required
def close_order(id):
    order = Order.query.filter(Order.id == id).first()
    if order is None:
        abort(404)
    if (current_user.id == order.courrier_id or current_user.is_admin()) and (
        order.stoptime is None or (order.stoptime > datetime.now())
    ):
        order.stoptime = datetime.now()
        if order.courrier_id == 0 or order.courrier_id is None:
            courrier = select_user(order.items)
            print(courrier)
            if courrier is not None:
                order.courrier_id = courrier.id
        db.session.commit()
        return redirect(url_for("order_bp.order", id=id))


def select_user(items):
    user = None
    # remove non users
    items = [i for i in items if i.user_id]

    if len(items) <= 0:
        return None

    while user is None:
        item = random.choice(items)
        user = item.user
        if user:
            if random.randint(user.bias, 100) < 80:
                user = None

    return user


def get_orders(expression=None):
    orders = []
    if expression is None:
        expression = (datetime.now() > Order.starttime) & (
            Order.stoptime > datetime.now()
        ) | (Order.stoptime == None)
    if not current_user.is_anonymous():
        orders = Order.query.filter(expression).all()
    else:
        orders = Order.query.filter((expression & (Order.public == True))).all()
    return orders
