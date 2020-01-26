"Script for everything Order related in the database"
import typing
from datetime import datetime

from .database import db
from .location import Location
from .user import User


class Order(db.Model):
    "Class used for configuring the Order model in the database"
    id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.String(64))
    location_name = db.Column(db.String(128))
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    public = db.Column(db.Boolean, default=True)

    items = db.relationship("OrderItem", backref="order", lazy="dynamic")

    def configure(self, courier: User, location: Location,
                  starttime: db.DateTime, stoptime: db.DateTime,) -> None:
        "Configure the Order"
        # pylint: disable=W0201
        self.courier = courier
        self.location = location
        self.starttime = starttime
        self.stoptime = stoptime

    def __repr__(self) -> str:
        # pylint: disable=R1705
        if self.location:
            return "Order %d @ %s" % (self.id, self.location.name or "None")
        else:
            return "Order %d" % (self.id)

    def group_by_user(self) -> typing.Dict[str, typing.Any]:
        "Group items of an Order by user"
        group: typing.Dict[str, typing.Any] = dict()
        for item in self.items:
            user = group.get(item.get_name(), dict())
            user["total"] = user.get("total", 0) + item.product.price
            user["to_pay"] = (
                user.get("to_pay", 0) +
                item.product.price if not item.paid else 0
            )
            user["paid"] = user.get("paid", True) and item.paid
            user["products"] = user.get("products", []) + [item.product]
            group[item.get_name()] = user

        return group

    def group_by_product(self) -> typing.Dict[str, typing.Any]:
        "Group items of an Order by product"
        group: typing.Dict[str, typing.Any] = dict()
        for item in self.items:
            product = group.get(item.product.name, dict())
            product["count"] = product.get("count", 0) + 1
            if item.extra:
                product["extras"] = product.get("extras", []) + [item.extra]
            group[item.product.name] = product

        return group

    def can_close(self, user_id: int) -> bool:
        "Check if a user can close the Order"
        if self.stoptime and self.stoptime < datetime.now():
            return False
        user = None
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            print(user)
        if self.courier_id == user_id or (user and user.is_admin()):
            return True
        return False
