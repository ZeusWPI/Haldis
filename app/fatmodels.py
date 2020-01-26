import typing

from sqlalchemy.sql import desc, func

from hlds.definitions import location_definitions
from hlds.models import Location, Dish
from models import Order, OrderItem, User


class FatModel:
    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def amount(cls):
        return cls.query.count()


class FatLocation(Location, FatModel):
    @classmethod
    def all(cls):
        return location_definitions

    @classmethod
    def amount(cls):
        return len(location_definitions)


class FatOrder(Order, FatModel):

    # It's hard to add the unique user constraint,
    #  as DISTINCT seems to apply after a GROUP BY and aggregate
    # So DISTINCT ... count(user_id) ... will count all users,
    #  even if they get reduced by the disctinct afterwards.
    @classmethod
    def items_per_order(cls):
        return (
            Order.query.join(OrderItem).group_by(Order.id)
            .with_entities(Order.id,
                           func.count(OrderItem.user_id).label("total"))
        )


class FatUser(User, FatModel):
    pass


class FatOrderItem(OrderItem, FatModel):
    pass


class FatDish(Dish, FatModel):
    @classmethod
    def top4(cls) -> None:
        top4 = (
            OrderItem.query
            .join(Order)
            .group_by(Order.location_id, OrderItem.dish_id)
            .with_entities(
                Order.location_id, OrderItem.dish_id, func.count(
                    OrderItem.dish_id).label("count")
            )
            .order_by(desc("count"))
            .limit(4)
        )
        for top in top4:
            print(top)
