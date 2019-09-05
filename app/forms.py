from datetime import datetime, timedelta

from flask import session
from flask_login import current_user
from flask_wtf import FlaskForm as Form
from wtforms import DateTimeField, SelectField, StringField, SubmitField, validators

from models import Location, User
from utils import euro_string


class OrderForm(Form):
    courrier_id = SelectField("Courrier", coerce=int)
    location_id = SelectField(
        "Location", coerce=int, validators=[validators.required()]
    )
    starttime = DateTimeField(
        "Starttime", default=datetime.now, format="%d-%m-%Y %H:%M"
    )
    stoptime = DateTimeField("Stoptime", format="%d-%m-%Y %H:%M")
    submit_button = SubmitField("Submit")

    def populate(self):
        if current_user.is_admin():
            self.courrier_id.choices = [(0, None)] + [
                (u.id, u.username) for u in User.query.order_by("username")
            ]
        else:
            self.courrier_id.choices = [
                (0, None),
                (current_user.id, current_user.username),
            ]
        self.location_id.choices = [
            (l.id, l.name) for l in Location.query.order_by("name")
        ]
        if self.stoptime.data is None:
            self.stoptime.data = datetime.now() + timedelta(hours=1)


class OrderItemForm(Form):
    product_id = SelectField("Item", coerce=int)
    extra = StringField("Extra")
    submit_button = SubmitField("Submit")

    def populate(self, location):
        self.product_id.choices = [
            (i.id, (i.name + ": " + euro_string(i.price))) for i in location.products
        ]


class AnonOrderItemForm(OrderItemForm):
    name = StringField("Name", validators=[validators.required()])

    def populate(self, location):
        OrderItemForm.populate(self, location)
        if self.name.data is None:
            self.name.data = session.get("anon_name", None)

    def validate(self):
        rv = OrderForm.validate(self)
        if not rv:
            return False

        # check if we have a user with this name
        user = User.query.filter_by(username=self.name.data).first()
        if user is not None:
            self.name.errors.append("Name already in use")
            return False
        return True
