"Script for everything OrderItemChoice related in the database"
from datetime import datetime

from .database import db
from .orderitem import OrderItem


class OrderItemChoice(db.Model):
    "Class used for configuring the OrderItemChoice model in the database"
    id = db.Column(db.Integer, primary_key=True)
    choice_id = db.Column(db.String(64), nullable=True)
    order_item_id = db.Column(
        db.Integer, db.ForeignKey("order_item.id"), nullable=False
    )
    kind = db.Column(db.String(1), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    value = db.Column(db.String(120), nullable=True)

    # pylint: disable=attribute-defined-outside-init
    def configure(self, order: OrderItem) -> None:
        "Set the orderitem"
        self.order = order

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"
