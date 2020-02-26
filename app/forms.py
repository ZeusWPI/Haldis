"Script for everything form related in Haldis"
from datetime import datetime, timedelta

from typing import Optional

from flask import session
from flask_login import current_user
from flask_wtf import FlaskForm as Form
from wtforms import (DateTimeField, SelectField, SelectMultipleField, StringField, SubmitField,
                     FieldList, validators)

from utils import euro_string
from hlds.definitions import location_definitions
from hlds.models import Location, Dish, Choice
from models import User


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
        self.location_id.choices = [
            (l.id, l.name) for l in location_definitions
        ]
        if self.stoptime.data is None:
            self.stoptime.data = datetime.now() + timedelta(hours=1)


class OrderItemForm(Form):
    "New Item in an Order"
    # pylint: disable=R0903
    dish_id = SelectField("Dish")
    comment = StringField("Comment")
    submit_button = SubmitField("Submit")

    @staticmethod
    def format_price_range(price_range):
        if price_range[0] == price_range[1]:
            return euro_string(price_range[0])
        else:
            return "from {}".format(euro_string(price_range[0]))

    def populate(self, location: Location) -> None:
        self.dish_id.choices = [
            (dish.id, (dish.name + ": " + self.format_price_range(dish.price_range())))
            for dish in location.dishes
        ]


class AnonOrderItemForm(OrderItemForm):
    """
    Class which defines the form for a new Item in an Order
    For Users who aren't logged in
    """
    name = StringField("Name", validators=[validators.required()])

    def populate(self, location: Location) -> None:
        """
        Fill in all the dish options from the location and
        the name of the anon user
        """
        OrderItemForm.populate(self, location)
        if self.name.data is None:
            self.name.data = session.get("anon_name", None)

    def validate(self) -> bool:
        "Check if the provided anon_name is not already taken"
        rv = OrderForm.validate(self)
        if not rv:
            return False

        # check if we have a user with this name
        user = User.query.filter_by(username=self.name.data).first()
        if user is not None:
            self.name.errors.append("Name already in use")
            return False
        return True
