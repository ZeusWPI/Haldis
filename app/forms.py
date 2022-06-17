"Script for everything form related in Haldis"
from datetime import datetime, timedelta
from typing import Optional

from flask import request, session
from flask_login import current_user
from flask_wtf import FlaskForm as Form
from hlds.definitions import location_definitions
from hlds.models import Choice, Dish, Location
from models import User
from utils import euro_string, price_range_string
from wtforms import (DateTimeField, FieldList, SelectField,
                     SelectMultipleField, StringField, SubmitField, validators)


class OrderForm(Form):
    "Class which defines the form for a new Order"
    # pylint: disable=R0903
    courier_id = SelectField("Courier", coerce=int)
    location_id = SelectField(
        "Location", coerce=str, validators=[validators.required()]
    )
    starttime = DateTimeField(
        "Starttime", default=datetime.now, format="%d-%m-%Y %H:%M"
    )
    stoptime = DateTimeField("Stoptime", format="%d-%m-%Y %H:%M")
    association = SelectField("Association", coerce=str, validators=[validators.required()])
    submit_button = SubmitField("Submit")

    def populate(self) -> None:
        "Fill in the options for courier for an Order"
        if current_user.is_admin():
            self.courier_id.choices = [(0, None)] + [
                (u.id, u.username) for u in User.query.order_by("username")
            ]
        else:
            self.courier_id.choices = [
                (0, None),
                (current_user.id, current_user.username),
            ]
        self.location_id.choices = [(l.id, l.name) for l in location_definitions]
        self.association.choices = current_user.association_list()
        if self.stoptime.data is None:
            self.stoptime.data = datetime.now() + timedelta(hours=1)


class OrderItemForm(Form):
    "New Item in an Order"
    # pylint: disable=R0903
    dish_id = SelectField("Dish")
    comment = StringField("Comment")
    submit_button = SubmitField("Submit")

    def populate(self, location: Location) -> None:
        "Populate the order item form"
        self.dish_id.choices = [(dish.id, dish.name) for dish in location.dishes]
        if not self.is_submitted() and self.comment.data is None:
            self.comment.data = request.args.get("comment")


class AnonOrderItemForm(OrderItemForm):
    """
    Class which defines the form for a new Item in an Order
    For Users who aren't logged in
    """

    user_name = StringField("Name", validators=[validators.required()])

    def populate(self, location: Location) -> None:
        """
        Fill in all the dish options from the location and
        the name of the anon user
        """
        OrderItemForm.populate(self, location)
        if not self.is_submitted():
            if self.user_name.data is None:
                self.user_name.data = request.args.get("user_name")
            if self.user_name.data is None:
                self.user_name.data = session.get("anon_name", None)

    def validate(self) -> bool:
        """Check if the provided anon_name is not already taken"""
        rv = OrderForm.validate(self)
        if not rv:
            return False

        # check if we have a user with this name
        user = User.query.filter_by(username=self.user_name.data).first()
        if user is not None:
            self.user_name.errors.append("Name already in use")
            return False
        return True
