"Module used for everything related to the fat versions of models"
import typing

from .hlds.definitions import location_definitions
from .hlds.models import Dish, Location
from .models import Order, OrderItem, User
from sqlalchemy.sql import desc, func


class FatModel:
    "General class for the fat version of models"

    @classmethod
    def all(cls):
        "Function to query all"
        # pylint: disable=E1101
        return cls.query.all()

    @classmethod
    def amount(cls):
        "Function to query the amount"
        # pylint: disable=E1101
        return cls.query.count()


class FatLocation(Location, FatModel):
    "Fat version of the Location model"

    @classmethod
    def all(cls):
        return location_definitions

    @classmethod
    def amount(cls):
        return len(location_definitions)


class FatOrder(Order, FatModel):
    "Fat version of the Order model"

    # It's hard to add the unique user constraint,
    #  as DISTINCT seems to apply after a GROUP BY and aggregate
    # So DISTINCT ... count(user_id) ... will count all users,
    #  even if they get reduced by the disctinct afterwards.
    @classmethod
    def items_per_order(cls):
        "Function to get the total of all items per order"
        return (Order.query.join(OrderItem).group_by(Order.id).with_entities(
            Order.id,
            func.count(OrderItem.user_id).label("total")))


class FatUser(User, FatModel):
    "Fat version of the User model"


class FatOrderItem(OrderItem, FatModel):
    "Fat version of the OrderItem model"
