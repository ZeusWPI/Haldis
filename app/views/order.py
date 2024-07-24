"""Script to generate the order related views of Haldis"""
from crypt import methods
import random
import re
import typing
from datetime import datetime, timedelta

# from flask import current_app as app
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   session, url_for, wrappers)
from flask_login import current_user, login_required
from ..forms import AnonOrderItemForm, OrderForm, OrderItemForm
from ..hlds.definitions import location_definition_version, location_definitions
from ..models import Order, OrderItem, User, db
from ..notification import post_order_to_webhook
from ..utils import ignore_none, parse_euro_string
from werkzeug.wrappers import Response

order_bp = Blueprint("order_bp", "order")


@order_bp.route("/")
def orders(form: OrderForm = None) -> str:
    """Generate general order view"""
    if form is None and current_user.association_list():
        form = OrderForm()
        location_id = request.args.get("location_id")
        form.location_id.default = location_id
        form.process()
        form.populate()
    return render_template("orders.html", orders=get_orders(), form=form)


@order_bp.route("/create", methods=["POST"])
@login_required
def order_create() -> typing.Union[str, Response]:
    """Generate order create view"""
    if not current_user.association_list():
        flash("Not allowed to create an order.", "info")
        abort(401)
    orderForm = OrderForm()
    orderForm.populate()
    if orderForm.validate_on_submit():
        order = Order()
        orderForm.populate_obj(order)
        order.update_from_hlds()
        db.session.add(order)
        db.session.commit()
        post_order_to_webhook(order)
        return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))
    return orders(form=orderForm)


@order_bp.route("/<order_slug>")
def order_from_slug(order_slug: str, form: OrderForm = None, dish_id=None) -> str:
    """Generate order view from id"""
    order: Order | None = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    if form is None:
        form = AnonOrderItemForm() if current_user.is_anonymous() else OrderItemForm()
        if order.location:
            form.populate(order.location)
    if order.is_closed():
        form = None
    total_price = sum(o.price or 0 for o in order.items)
    debts = sum(o.price or 0 for o in order.items if not o.paid)

    dish = order.location.dish_by_id(dish_id) if order.location else None

    return render_template(
        "order.html",
        order=order,
        form=form,
        total_price=total_price,
        debts=debts,
        selected_dish=dish,
    )


@order_bp.route("/<order_slug>/items")
def items_shop_view(order_slug: int) -> str:
    """Generate order items view from id"""
    order = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if current_user.is_anonymous() and not order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    total_price = sum(o.price or 0 for o in order.items)
    return render_template("order_items.html", order=order, total_price=total_price)

@order_bp.route("/<order_slug>/extend", methods=["POST"])
def order_extend(order_slug: str):
    """Extend an order"""
    order: Order | None = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if current_user.id is not order.courier_id and not current_user.is_admin():
        abort(401)

    if order.is_closed():
        order.stoptime = datetime.now() + timedelta(minutes=3)
    else:
        order.stoptime = order.stoptime + timedelta(minutes=3)
    db.session.commit()
    return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))


@order_bp.route("/<order_slug>/edit", methods=["GET", "POST"])
@login_required
def order_edit(order_slug: str) -> typing.Union[str, Response]:
    """Generate order edit view from id"""
    order = Order.query.filter(Order.slug == order_slug).first()
    if current_user.id is not order.courier_id and not current_user.is_admin():
        abort(401)
    if order is None:
        abort(404)
    order_form = OrderForm(obj=order)
    order_form.populate()
    if order_form.validate_on_submit():
        order_form.populate_obj(order)
        order.update_from_hlds()
        db.session.commit()
        return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))
    return render_template("order_edit.html", form=order_form, order_slug=order.slug)


@order_bp.route("/<order_slug>/create", methods=["GET", "POST"])
def order_item_create(order_slug: str) -> typing.Any:
    # type is 'typing.Union[str, Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    """Add item to order from slug"""
    current_order = Order.query.filter(Order.slug == order_slug).first()
    if current_order is None:
        abort(404)
    if current_order.is_closed():
        abort(404)
    if current_user.is_anonymous() and not current_order.public:
        flash("Please login to see this order.", "info")
        abort(401)
    location = current_order.location
    # If location doesn't exist anymore, adding items is nonsensical
    if not location:
        abort(404)
    form = AnonOrderItemForm() if current_user.is_anonymous() else OrderItemForm()

    dish_id = (
        request.form["dish_id"] if form.is_submitted() else request.args.get("dish")
    )
    if dish_id and not location.dish_by_id(dish_id):
        abort(404)
    if not form.is_submitted():
        form.dish_id.data = dish_id
    form.populate(current_order.location)

    if form.is_submitted():
        form_for_dish = request.form["dish_id"]
        dish_was_changed = form_for_dish != "" and form_for_dish != dish_id

        # The form's validation tests that dish_id is valid and gives a friendly error if it's not
        choices = location.dish_by_id(form.dish_id.data).choices
        chosen = [
            (
                choice.option_by_id(request.form.get("choice_" + choice.id))
                if choice_type == "single_choice"
                else list(
                    ignore_none(
                        request.form.getlist(
                            "choice_" + choice.id, type=choice.option_by_id
                        )
                    )
                )
            )
            for (choice_type, choice) in choices
        ]
        all_choices_present = all(x is not None for x in chosen)

        if dish_was_changed or not all_choices_present:
            try:
                user_name = (
                    form.user_name.data if form.user_name.validate(form) else None
                )
            except AttributeError:
                user_name = None
            comment = form.comment.data if form.comment.validate(form) else None

            return redirect(
                url_for(
                    "order_bp.order_item_create",
                    order_slug=current_order.slug,
                    dish=form.dish_id.data,
                    user_name=user_name,
                    comment=comment,
                )
            )

    # If the form was not submitted (GET request) or the form had errors: show form again
    if not form.validate_on_submit():
        return order_from_slug(current_order.slug, form=form, dish_id=dish_id)

    # Form was submitted and is valid
    item = OrderItem()
    form.populate_obj(item)
    item.hlds_data_version = location_definition_version
    item.order_id = current_order.id
    if not current_user.is_anonymous():
        item.user_id = current_user.id
    else:
        session["anon_name"] = item.user_name

    # XXX Temporary until OrderItemChoice is used
    def _name(option):
        no_text_tag = "no_text"
        try:
            if not option or no_text_tag in option.tags:
                return None
            return option.name
        except AttributeError:
            return ", ".join(o.name for o in option if no_text_tag not in o.tags)

    comments = list(ignore_none(_name(option) for option in chosen))
    if item.comment:
        comments.append("Comment: " + item.comment)
    item.comment = "; ".join(comments)

    item.update_from_hlds()

    # XXX Temporary until OrderItemChoice is used. Move this price calculation to update_from_hlds
    # when in OrderItemChoice is in place.
    def _price(option):
        try:
            return option.price or 0
        except AttributeError:
            return sum(o.price or 0 for o in option)

    item.price += sum(_price(option) for option in chosen)

    db.session.add(item)
    db.session.commit()
    flash("Ordered %s" % item.dish_name, "success")
    return redirect(url_for("order_bp.order_from_slug", order_slug=order_slug))


@order_bp.route("/<order_slug>/modify_items", methods=["POST"])
@login_required
# pylint: disable=R1710
def modify_items(order_slug: str) -> typing.Optional[Response]:
    if "delete_item" in request.form:
        return delete_item(order_slug, int(request.form["delete_item"]))
    user_names = request.form.getlist("user_names")
    if request.form.get("action") == "mark_paid":
        return set_items_paid(order_slug, user_names, True)
    elif request.form.get("action") == "mark_unpaid":
        return set_items_paid(order_slug, user_names, False)
    else:
        abort(404)
        return None

def set_items_paid(order_slug: str, user_names: typing.Iterable[str], paid: bool):
    order = Order.query.filter(Order.slug == order_slug).first()
    total_paid_items = 0
    total_failed_items = 0
    for user_name in user_names:
        user = User.query.filter(User.username == user_name).first()
        items: typing.List[OrderItem] = []
        if user:
            items = OrderItem.query.filter(
                (OrderItem.user_id == user.id) & (OrderItem.order_id == order.id)
            ).all()
        else:
            items = OrderItem.query.filter(
                (OrderItem.user_name == user_name) & (OrderItem.order_id == order.id)
            ).all()

        for item in items:
            if item.can_modify_payment(order.id, current_user.id):
                if item.paid != paid:
                    item.paid = paid
                    total_paid_items += 1
            else:
                total_failed_items += 1

    db.session.commit()
    if total_failed_items == 0:
        flash("Marked %d items as paid" % (total_paid_items,), "success")
    else:
        flash("Failed to mark %d items as paid (succeeded in marking %d items as paid)" % (total_failed_items, total_paid_items), "error")
    return redirect(url_for("order_bp.order_from_slug", order_slug=order_slug))


@order_bp.route("/<order_slug>/<item_id>/delete", methods=["POST"])
# pylint: disable=R1710
def delete_item(order_slug: str, item_id: int) -> typing.Any:
    # type is 'typing.Optional[Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    """Delete an item from an order"""
    item: OrderItem = OrderItem.query.filter(OrderItem.id == item_id).first()
    order: Order = Order.query.filter(Order.slug == order_slug).first()
    user_id = None
    if not current_user.is_anonymous():
        user_id = current_user.id
    if item.can_delete(order.id, user_id, session.get("anon_name", "")):
        dish_name = item.dish_name
        db.session.delete(item)
        db.session.commit()
        flash("Deleted %s" % dish_name, "success")
        return redirect(url_for("order_bp.order_from_slug", order_slug=order_slug))
    abort(404)


@order_bp.route("/<order_slug>/volunteer", methods=["POST"])
@login_required
def volunteer(order_slug: str) -> Response:
    """Add a volunteer to an order"""
    order = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if order.courier_id is None or order.courier_id == 0:
        order.courier_id = current_user.id
        db.session.commit()
        flash("Thank you for volunteering!")
    else:
        flash("Volunteering not possible!")
    return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))


@order_bp.route("/<order_slug>/close", methods=["POST"])
@login_required
def close_order(order_slug: str) -> typing.Optional[Response]:
    """Close an order"""
    order = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if (
        current_user.id == order.courier_id or current_user.is_admin()
    ) and not order.is_closed():
        order.stoptime = datetime.now()
        if order.courier_id == 0 or order.courier_id is None:
            courier = select_user(order.items)
            if courier is not None:
                order.courier_id = courier.id
        db.session.commit()
        return redirect(url_for("order_bp.order_from_slug", order_slug=order_slug))
    return None


@order_bp.route("/<order_slug>/prices", methods=["GET", "POST"])
@login_required
def prices(order_slug: str) -> typing.Optional[Response]:
    order = Order.query.filter(Order.slug == order_slug).first()
    if order is None:
        abort(404)
    if not order.can_modify_prices(current_user.id):
        flash("You cannot modify the prices at this time.", "error")
        return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))

    if request.method == "GET":
        return render_template(
            "order_prices.html",
            order=order,
        )
    else:
        new_prices = {}

        for key, value in request.form.items():
            m = re.fullmatch("item_([0-9]+)", key)
            if not m:
                continue
            item_id = int(m.group(1))

            price = parse_euro_string(value)
            if not price:
                flash(f"Could not recognize '{value}' as a price")
                continue

            new_prices[item_id] = price

        for item in order.items:
            new_price = new_prices.get(item.id)
            if new_price is not None and new_price != item.price:
                item.price = new_price
                item.price_modified = datetime.now()
        db.session.commit()

    return redirect(url_for("order_bp.order_from_slug", order_slug=order.slug))



def select_user(items) -> typing.Optional[User]:
    """Select a random user from those who are signed up for the order"""
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
    """Give the list of all currently open and public Orders"""
    order_list: typing.List[OrderForm] = []
    if expression is None:
        expression = ((datetime.now() > Order.starttime) & (
                Order.stoptime
                > datetime.now()
                # pylint: disable=C0121
            ) | (Order.stoptime == None)
        ) & (Order.association.in_(current_user.association_list()))
    if not current_user.is_anonymous():
        order_list = Order.query.filter(expression).all()
    else:
        order_list = Order.query.filter(
            # pylint: disable=C0121
            expression & (Order.public == True) & (Order.association.in_(current_user.association_list()))
        ).all()
    return order_list
