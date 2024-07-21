"""Script for everything Order related in the database"""
import typing
from collections import defaultdict
from datetime import datetime
import secrets
import string

from ..hlds.definitions import location_definitions
from ..utils import first

from .database import db
from .user import User

BASE31_ALPHABET = '23456789abcdefghjkmnpqrstuvwxyz'

def generate_slug():
    secret = ''.join(secrets.choice(BASE31_ALPHABET) for i in range(8))
    while Order.query.filter(Order.slug == secret).first() is not None:
        secret = ''.join(secrets.choice(BASE31_ALPHABET) for i in range(8))
    return secret

class Order(db.Model):
    """Class used for configuring the Order model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.String(64))
    location_name = db.Column(db.String(128))
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    public = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(8), default=generate_slug, unique=True)
    association = db.Column(db.String(120), nullable=False, server_default="")

    items = db.relationship("OrderItem", backref="order", lazy="dynamic")

    def __getattr__(self, name):
        if name == "location":
            return first(
                filter(lambda l: l.id == self.location_id, location_definitions)
            )
        raise AttributeError()

    def __repr__(self) -> str:
        # pylint: disable=R1705
        if self.location:
            return f"Order {self.id} @ {self.location.name or 'None'}"
        else:
            return f"Order {self.id}"

    def update_from_hlds(self) -> None:
        """
        Update the location name from the HLDS definition.
        User should commit after running this to make the change persistent.
        """
        assert (
            self.location_id
        ), "location_id must be configured before updating from .hlds"
        self.location_name = self.location.name

    def for_user(self, anon=None, user=None) -> typing.List:
        """Get the items for a certain user"""
        return list(
            filter(
                (lambda i: i.user == user)
                if user is not None
                else (lambda i: i.user_name == anon),
                self.items,
            )
        )

    def group_by_user(self) -> typing.List[typing.Tuple[str, typing.List]]:
        """Group items of an Order by user"""
        group: typing.Dict[str, typing.List] = {}

        # pylint: disable=E1133
        for item in self.items:
            if item.for_name not in group:
                group[item.for_name] = []

            group[item.for_name].append(item)

        for _user_name, order_items in group.items():
            order_items.sort(key=lambda order_item: order_item.comment or "")

        return list(sorted(group.items(), key=lambda t: (t[0] or "", t[1] or "")))

    def group_by_dish(
        self,
    ) -> typing.List[
        typing.Tuple[str, int, typing.List[typing.Tuple[str, typing.List]]]
    ]:
        """Group items of an Order by dish"""
        group: typing.Dict[str, typing.Dict[str, typing.List]] = defaultdict(
            lambda: defaultdict(list)
        )

        # pylint: disable=E1133
        for item in self.items:
            group[item.dish_name][item.comment].append(item)

        return sorted(
            (
                dish_name,
                # Amount of items of this dish
                sum(map(len, comment_group.values())),
                sorted(
                    (comment, sorted(items, key=lambda x: (x.for_name or "")))
                    for comment, items in comment_group.items()
                ),
            )
            for dish_name, comment_group in group.items()
        )

    def is_closed(self) -> bool:
        """Return whether the order is closed"""
        return self.stoptime and datetime.now() > self.stoptime

    def can_close(self, user_id: int) -> bool:
        """Check if a user can close the Order"""
        if self.stoptime and self.stoptime < datetime.now():
            return False
        user = None
        if user_id:
            user = User.query.filter_by(id=user_id).first()
        if self.courier_id == user_id or (user and user.is_admin()):
            return True
        return False

    def can_modify_prices(self, user_id: int) -> bool:
        if not self.is_closed():
            return False
        user = User.query.filter_by(id=user_id).first()
        return user and (user.is_admin() or user == self.courier)

    def can_modify_payment(self, user_id: int) -> bool:
        user = User.query.filter_by(id=user_id).first()
        return user and (user.is_admin() or user == self.courier)
