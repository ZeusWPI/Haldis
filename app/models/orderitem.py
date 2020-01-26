"Script for everything OrderItem related in the database"
from datetime import datetime

from .database import db
from .order import Order
from .user import User


class OrderItem(db.Model):
    "Class used for configuring the OrderItem model in the database"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_name = db.Column(db.String(120))
    dish_id = db.Column(db.String(120), nullable=True)
    dish_name = db.Column(db.String(120), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    paid = db.Column(
        db.Boolean, default=False, nullable=False
    )
    comment = db.Column(db.Text(), nullable=True)
    hlds_data_version = db.Column(db.String(40), nullable=True)

    choices = db.relationship("OrderItemChoice", backref="order_item", lazy="dynamic")

    def configure(self, user: User, order: Order) -> None:
        "Configure the OrderItem"
        # pylint: disable=W0201
        self.user = user
        self.order = order

    def get_name(self) -> str:
        "Get the name of the user which 'owns' the item"
        if self.user_id is not None and self.user_id > 0:
            return self.user.username
        return self.name

    def __repr__(self) -> str:
        return "Order %d: %s wants %s" % (
            self.order_id or 0,
            self.get_name(),
            self.dish_name or "None",
        )

    # pylint: disable=W0613
    def can_delete(self, order_id: int, user_id: int, name: str) -> bool:
        "Check if a user can delete an item"
        if int(self.order_id) != int(order_id):
            return False
        if self.order.stoptime and self.order.stoptime < datetime.now():
            return False
        if self.user is not None and self.user_id == user_id:
            return True
        if user_id is None:
            return False
        user = User.query.filter(User.id == user_id).first()
        if user and (user.is_admin() or user == self.order.courier):
            return True
        return False
