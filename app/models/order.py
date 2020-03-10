"Script for everything Order related in the database"
import typing
from datetime import datetime

from utils import first
from hlds.definitions import location_definitions
from .database import db
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

    def __getattr__(self, name):
        if name == "location":
            return first(filter(lambda l: l.id == self.location_id, location_definitions))
        raise AttributeError()

    def __repr__(self) -> str:
        # pylint: disable=R1705
        if self.location:
            return "Order %d @ %s" % (self.id, self.location.name or "None")
        else:
            return "Order %d" % (self.id)

    def update_from_hlds(self) -> None:
        """
        Update the location name from the HLDS definition.
        User should commit after running this to make the change persistent.
        """
        assert self.location_id, "location_id must be configured before updating from HLDS"
        self.location_name = self.location.name

    def group_by_user(self) -> typing.Dict[str, typing.Any]:
        "Group items of an Order by user"
        group: typing.Dict[str, typing.Any] = dict()
        for item in self.items:
            user = group.get(item.get_name(), dict())
            user["total"] = user.get("total", 0) + item.price
            user["to_pay"] = (
                user.get("to_pay", 0) +
                item.price if not item.paid else 0
            )
            user["paid"] = user.get("paid", True) and item.paid
            user["dishes"] = user.get("dishes", []) + [item.dish_name]
            group[str(item.get_name())] = user

        return group

    def group_by_dish(self, sort_comments=False) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
        "Group items of an Order by dish"
        group: typing.Dict[str, typing.Dict[str, typing.Any]] = dict()
        for item in self.items:
            dish = group.get(item.dish_name, dict())
            dish["count"] = dish.get("count", 0) + 1
            dish["comments"] = dish.get("comments", []) + [item.comment]
            group[item.dish_name] = dish

        if sort_comments:
            for _dish_name, dish_props in group.items():
                dish_props["comments"].sort()

        return group

    def is_closed(self) -> bool:
        return self.stoptime and datetime.now() > self.stoptime

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
