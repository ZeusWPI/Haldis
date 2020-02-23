"Script to generate the order related views of Haldis"
import random
import typing
from datetime import datetime

from werkzeug.wrappers import Response
# from flask import current_app as app
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   session, url_for, wrappers)
from flask_login import current_user, login_required

from forms import AnonOrderItemForm, OrderForm, OrderItemForm
from models import Order, OrderItem, User, db
from hlds.definitions import location_definitions
from notification import post_order_to_webhook
from utils import ignore_none

order_bp = Blueprint("order_bp", "order")


@order_bp.route("/")
def orders(form: OrderForm = None) -> str:
    "Generate general order view"
    if form is None and not current_user.is_anonymous():
        form = OrderForm()
        location_id = request.args.get("location_id")
        form.location_id.default = location_id
        form.process()
        form.populate()
    return render_template("orders.html", orders=get_orders(), form=form)


@order_bp.route("/create", methods=["POST"])
@login_required
def order_create() -> typing.Union[str, Response]:
    "Generate order create view"
    orderForm = OrderForm()
    orderForm.populate()
    if orderForm.validate_on_submit():
        order = Order()
        orderForm.populate_obj(order)
        order.update_from_hlds()
        db.session.add(order)
        db.session.commit()
        post_order_to_webhook(order)
        return redirect(url_for("order_bp.order_from_id", order_id=order.id))
    return orders(form=orderForm)


@order_bp.route("/<order_id>")
def order_from_id(order_id: int, form: OrderForm = None, dish_id=None) -> str:
    "Generate order view from id"
    order = Order.query.filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    if form is None:
        form = AnonOrderItemForm() if current_user.is_anonymous() \
            else OrderItemForm()
        if order.location:
            form.populate(order.location, None)
    if order.is_closed():
        form = None
    total_price = sum([o.price for o in order.items])
    debts = sum([o.price for o in order.items if not o.paid])

    dish = order.location.dish_by_id(dish_id) if order.location else None

    return render_template("order.html", order=order, form=form,
                           total_price=total_price, debts=debts, dish=dish)


@order_bp.route("/<order_id>/items")
def items_showcase(order_id: int) -> str:
    "Generate order items view from id"
    order = Order.query.filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    total_price = sum([o.price for o in order.items])
    return render_template("order_items.html", order=order, total_price=total_price)


@order_bp.route("/<order_id>/edit", methods=["GET", "POST"])
@login_required
def order_edit(order_id: int) -> typing.Union[str, Response]:
    "Generate order edit view from id"
    order = Order.query.filter(Order.id == order_id).first()
    if current_user.id is not order.courier_id and \
            not current_user.is_admin():
        abort(401)
    if order is None:
        abort(404)
    orderForm = OrderForm(obj=order)
    orderForm.populate()
    if orderForm.validate_on_submit():
        orderForm.populate_obj(order)
        order.update_from_hlds()
        db.session.commit()
        return redirect(url_for("order_bp.order_from_id", order_id=order.id))
    return render_template("order_edit.html", form=orderForm,
                           order_id=order_id)

def _name(option):
    try:
        return option.name
    except AttributeError:
        return ", ".join(o.name for o in option)

@order_bp.route("/<order_id>/create", methods=["GET", "POST"])
def order_item_create(order_id: int) -> typing.Any:
    # type is 'typing.Union[str, Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    "Add item to order from id"
    current_order = Order.query.filter(Order.id == order_id).first()
    if current_order is None:
        abort(404)
    if current_order.is_closed():
        abort(404)
    if current_user.is_anonymous() and not current_order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    location = current_order.location
    # If location doesn't exist any more, adding items is nonsensical
    if not location:
        abort(404)
    form = AnonOrderItemForm() if current_user.is_anonymous() \
        else OrderItemForm()

    dish_id_in_url = request.args.get("dish")
    dish_id = form.dish_id.data if form.is_submitted() else dish_id_in_url
    if dish_id and not location.dish_by_id(dish_id):
        abort(404)
    form.dish_id.data = dish_id
    form.populate(current_order.location, dish_id)

    # If the form was not submitted (GET request), the form had errors, or the dish was changed: show form again
    if not form.validate_on_submit() or (dish_id_in_url and dish_id_in_url != dish_id):
        return order_from_id(order_id, form=form, dish_id=dish_id)

    # Form was submitted and is valid

    # The form's validation tests that dish_id is valid and gives a friendly error if it's not
    choices = location.dish_by_id(form.dish_id.data).choices
    chosen = [
        (
            choice.option_by_id(request.form.get("choice_" + choice.id))
            if choice_type == "single_choice" else
            list(ignore_none(request.form.getlist("choice_" + choice.id, type=choice.option_by_id)))
        )
        for (choice_type, choice) in choices
    ]
    all_choices_present = all(x is not None for x in chosen)
    if not all_choices_present:
        return redirect(url_for("order_bp.order_item_create",
                                order_id=order_id, dish=form.dish_id.data))

    item = OrderItem()
    form.populate_obj(item)
    item.order_id = order_id
    if not current_user.is_anonymous():
        item.user_id = current_user.id
    else:
        session["anon_name"] = item.name

    # XXX Temporary
    comments = [_name(option) for option in chosen if option]
    if item.comment:
        comments.append("Comment: " + item.comment)
    item.comment = "; ".join(comments)

    item.update_from_hlds()
    db.session.add(item)
    db.session.commit()
    flash("Ordered %s" % (item.dish_name), "success")
    return redirect(url_for("order_bp.order_from_id", order_id=order_id))


@order_bp.route("/<order_id>/<item_id>/paid", methods=["POST"])
@login_required
# pylint: disable=R1710
def item_paid(order_id: int, item_id: int) -> typing.Optional[Response]:
    "Indicate payment status for an item in an order"
    item = OrderItem.query.filter(OrderItem.id == item_id).first()
    user_id = current_user.id
    if item.order.courier_id == user_id or current_user.admin:
        item.paid = True
        db.session.commit()
        flash("Paid %s by %s" % (item.dish_name, item.get_name()),
              "success")
        return redirect(url_for("order_bp.order_from_id", order_id=order_id))
    abort(404)


@order_bp.route("/<order_id>/<user_name>/user_paid", methods=["POST"])
@login_required
# pylint: disable=R1710
def items_user_paid(order_id: int, user_name: str) -> typing.Optional[Response]:
    "Indicate payment status for a user in an order"
    user = User.query.filter(User.username == user_name).first()
    items: typing.List[OrderItem] = []
    if user:
        items = OrderItem.query.filter(
            (OrderItem.user_id == user.id) & (OrderItem.order_id == order_id)
        ).all()
    else:
        items = OrderItem.query.filter(
            (OrderItem.name == user_name) & (OrderItem.order_id == order_id)
        ).all()
    current_order = Order.query.filter(Order.id == order_id).first()
    for item in items:
        print(item)
    if current_order.courier_id == current_user.id or current_user.admin:
        for item in items:
            item.paid = True
        db.session.commit()
        flash("Paid %d items for %s" %
              (len(items), item.get_name()), "success")
        return redirect(url_for("order_bp.order_from_id", order_id=order_id))
    abort(404)


@order_bp.route("/<order_id>/<item_id>/delete", methods=["POST"])
# pylint: disable=R1710
def delete_item(order_id: int, item_id: int) -> typing.Any:
    # type is 'typing.Optional[Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    "Delete an item from an order"
    item = OrderItem.query.filter(OrderItem.id == item_id).first()
    user_id = None
    if not current_user.is_anonymous():
        print("%s tries to delete orders" % (current_user.username))
        user_id = current_user.id
    if item.can_delete(order_id, user_id, session.get("anon_name", "")):
        dish_name = item.dish_name
        db.session.delete(item)
        db.session.commit()
        flash("Deleted %s" % (dish_name), "success")
        return redirect(url_for("order_bp.order_from_id", order_id=order_id))
    abort(404)


@order_bp.route("/<order_id>/volunteer", methods=["POST"])
@login_required
def volunteer(order_id: int) -> Response:
    "Add a volunteer to an order"
    order = Order.query.filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    if order.courier_id is None or order.courier_id == 0:
        order.courier_id = current_user.id
        db.session.commit()
        flash("Thank you for volunteering!")
    else:
        flash("Volunteering not possible!")
    return redirect(url_for("order_bp.order_from_id", order_id=order_id))


@order_bp.route("/<order_id>/close", methods=["POST"])
@login_required
def close_order(order_id: int) -> typing.Optional[Response]:
    "Close an order"
    order = Order.query.filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    if (current_user.id == order.courier_id or current_user.is_admin()) and not order.is_closed():
        order.stoptime = datetime.now()
        if order.courier_id == 0 or order.courier_id is None:
            courier = select_user(order.items)
            print(courier)
            if courier is not None:
                order.courier_id = courier.id
        db.session.commit()
        return redirect(url_for("order_bp.order_from_id", order_id=order_id))
    # The line below is to make sure mypy doesn't say
    #   "Missing return statement"
    #   https://github.com/python/mypy/issues/4223
    return None


def select_user(items) -> typing.Optional[User]:
    "Select a random user from those who are signed up for the order"
    user = None
    # remove non users
    items = [i for i in items if i.user_id]

    if not items:
        return None

    while user is None:
        item = random.choice(items)
        user = item.user
        if user:
            if random.randint(user.bias, 100) < 80:
                user = None

    return user


def get_orders(expression=None) -> typing.List[Order]:
    "Give the list of all currently open and public Orders"
    order_list: typing.List[OrderForm] = []
    if expression is None:
        expression = (datetime.now() > Order.starttime) & (
            Order.stoptime > datetime.now()
            # pylint: disable=C0121
        ) | (Order.stoptime == None)
    if not current_user.is_anonymous():
        order_list = Order.query.filter(expression).all()
    else:
        order_list = Order.query.filter(
            # pylint: disable=C0121
            (expression & (Order.public == True))).all()
    return order_list
