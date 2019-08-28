# This file will expose what we want from the models module
# This will probably be everything. But putting the imports here makes it possible to import all models in one line like this:
#
# from models import User, Item, ...
#
# Instead of this:
# from models.user import User
# from models.item import Item
# ...

from .database import db
from .location import Location
from .order import Order
from .orderitem import OrderItem
from .product import Product
from .user import User
