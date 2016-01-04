from datetime import datetime
from collections import defaultdict

from app import db


# Create database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    runs = db.relation('Order', backref='courrier', primaryjoin='Order.courrier_id==User.id',
                       foreign_keys='Order.courrier_id')
    orderItems = db.relationship('OrderItem', backref='user', lazy='dynamic')

    def configure(self, username, admin, bias):
        self.username = username
        self.admin = admin
        self.bias = bias

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_admin(self):
        return self.admin

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '%s' % self.username


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(254))
    website = db.Column(db.String(120))
    telephone = db.Column(db.String(20), nullable=True)
    products = db.relationship('Product', backref='location', lazy='dynamic')
    orders = db.relationship('Order', backref='location', lazy='dynamic')

    def configure(self, name, address, website):
        self.name = name
        self.address = address
        self.website = website

    def __repr__(self):
        return '%s' % (self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orderItems = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def configure(self, location, name, price):
        self.location = location
        self.name = name
        self.price = price

    def __repr__(self):
        return '%s (€%d)from %s' % (self.name, self.price/100, self.location or 'None')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courrier_id = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    public = db.Column(db.Boolean, default=True)
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def configure(self, courrier, location, starttime, stoptime):
        self.courrier = courrier
        self.location = location
        self.starttime = starttime
        self.stoptime = stoptime

    def __repr__(self):
        return 'Order %d @ %s' % (self.id, self.location.name or 'None')

    def group_by_user(self):
        group = dict()
        for item in self.items:
            user = group.get(item.get_name(), dict())
            user["total"] = user.get("total", 0) + item.product.price
            user["to_pay"] = user.get("to_pay", 0) + item.product.price if not item.paid else 0
            user["paid"] = user.get("paid", True) and item.paid
            user["products"] = user.get("products", []) + [item.product]
            group[item.get_name()] = user

        return group

    def group_by_product(self):
        group = dict()
        for item in self.items:
            product = group.get(item.product.name, dict())
            product['count'] = product.get("count", 0) + 1
            if item.extra:
                product["extras"] = product.get("extras", []) + [item.extra]
            group[item.product.name] = product

        return group

    def can_close(self, user_id):
        if self.stoptime and self.stoptime < datetime.now():
            return False
        user = None
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            print(user)
        if self.courrier_id == user_id or (user and user.is_admin()):
            return True
        return False


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=False)
    extra = db.Column(db.String(254), nullable=True)
    name = db.Column(db.String(120))

    def configure(self, user, order, product):
        self.user = user
        self.order = order
        self.product = product

    def get_name(self):
        if self.user_id is not None and self.user_id > 0:
            return self.user.username
        return self.name

    def __repr__(self):
        product_name = None
        if self.product:
            product_name = self.product.name
        return 'Order %d: %s wants %s' % (self.order_id or 0, self.get_name(), product_name or 'None')

    def can_delete(self, order_id, user_id, name):
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
