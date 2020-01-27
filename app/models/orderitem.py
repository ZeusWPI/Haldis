"Script for everything OrderItem related in the database"
from datetime import datetime

from utils import first
from hlds.definitions import location_definitions
from .database import db
from .order import Order
from .user import User


class OrderItem(db.Model):
    "Class used for configuring the OrderItem model in the database"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_name = db.Column(db.String(120))
    dish_id = db.Column(db.String(64), nullable=True)
    dish_name = db.Column(db.String(120), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    paid = db.Column(
        db.Boolean, default=False, nullable=True
    )
    comment = db.Column(db.Text(), nullable=True)
    hlds_data_version = db.Column(db.String(40), nullable=True)

    choices = db.relationship("OrderItemChoice", backref="order_item", lazy="dynamic")

    def __getattr__(self, name):
        if name == "dish":
            location_id = Order.query.filter(Order.id == self.order_id).first().location_id
            location = first(filter(lambda l: l.id == location_id, location_definitions))
            if location:
                return first(filter(lambda d: d.id == self.dish_id, location.dishes))
            else:
                raise ValueError("No Location found with id: " + location_id)
        raise AttributeError()

    def get_name(self) -> str:
        "Get the name of the user which 'owns' the item"
        if self.user_id is not None and self.user_id > 0:
            return self.user.username
        return self.user_name

    def __repr__(self) -> str:
        return "Order %d: %s wants %s" % (
            self.order_id or 0,
            self.get_name(),
            self.dish_name or "None",
        )

    def update_from_hlds(self) -> None:
        """
        Update the dish name and price from the HLDS definition.
        User should commit after running this to make the change persistent.
        """
        assert self.order_id, "order_id must be configured before updating from HLDS"
        assert self.dish_id, "dish_id must be configured before updating from HLDS"
        self.dish_name = self.dish.name
        self.price = self.dish.price

    # pylint: disable=W0613
    def can_delete(self, order_id: int, user_id: int, name: str) -> bool:
        "Check if a user can delete an item"
        if int(self.order_id) != int(order_id):
            return False
        if self.order.is_closed():
            return False
        if self.user is not None and self.user_id == user_id:
            return True
        if user_id is None:
            return False
        user = User.query.filter(User.id == user_id).first()
        if user and (user.is_admin() or user == self.order.courier):
            return True
        return False
