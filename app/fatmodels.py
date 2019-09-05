from sqlalchemy.sql import desc, func

from models import Location, Order, OrderItem, Product, User


class FatModel:
    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def amount(cls):
        return cls.query.count()


class FatLocation(Location, FatModel):
    pass


class FatOrder(Order, FatModel):

    # It's hard to add the unique user constraint,
    #  as DISTINCT seems to apply after a GROUP BY and aggregate
    # So DISTINCT ... count(user_id) ... will count all users,
    #  even if they get reduced by the disctinct afterwards.
    @classmethod
    def items_per_order(cls):
        return (
            Order.query.join(OrderItem)
            .group_by(Order.id)
            .with_entities(Order.id, func.count(OrderItem.user_id).label("total"))
        )


class FatUser(User, FatModel):
    pass


class FatOrderItem(OrderItem, FatModel):
    pass


class FatProduct(Product, FatModel):
    @classmethod
    def top4(cls):
        top4 = (
            OrderItem.query.join(Product)
            .join(Location)
            .group_by(Product.id)
            .with_entities(
                Product.name, Location.name, func.count(Product.id).label("count")
            )
            .order_by(desc("count"))
            .limit(4)
        )
        for top in top4:
            print(top)
