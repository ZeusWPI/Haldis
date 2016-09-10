from models import User, Location, Order, OrderItem


class CountableModel:

    @classmethod
    def amount(cls):
        return cls.query.count()


class FatLocation(Location, CountableModel): pass


class FatOrder(Order, CountableModel): pass


class FatUser(User, CountableModel): pass


class FatOrderItem(OrderItem, CountableModel): pass
