from datetime import datetime

from .database import db
from .order import Order
from .product import Product
from .user import User


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=True
    )  # TODO make false after init migration
    paid = db.Column(
        db.Boolean, default=False, nullable=True
    )  # TODO make false after init migration
    extra = db.Column(db.String(254), nullable=True)
    name = db.Column(db.String(120))

    def configure(self, user: User, order: Order, product: Product) -> None:
        self.user = user
        self.order = order
        self.product = product

    def get_name(self) -> str:
        if self.user_id is not None and self.user_id > 0:
            return self.user.username
        return self.name

    def __repr__(self) -> str:
        product_name = None
        if self.product:
            product_name = self.product.name
        return "Order %d: %s wants %s" % (
            self.order_id or 0,
            self.get_name(),
            product_name or "None",
        )

    def can_delete(self, order_id: int, user_id: int, name: str) -> bool:
        if int(self.order_id) != int(order_id):
            return False
        if self.order.stoptime and self.order.stoptime < datetime.now():
            return False
        if self.user is not None and self.user_id == user_id:
            return True
        if user_id is None:
            return False
        user = User.query.filter(User.id == user_id).first()
        if user and user.is_admin():
            return True
        return False
