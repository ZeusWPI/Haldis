from datetime import datetime
from collections import defaultdict

from app import db


# Create database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    runs = db.relationship('Order', backref='courrier', lazy='dynamic')
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
    name = db.Column(db.String(120))
    address = db.Column(db.String(254))
    website = db.Column(db.String(120))
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
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    orderItems = db.relationship('OrderItem', backref='product', lazy='dynamic')


    def configure(self, location, name, price):
        self.location = location
        self.name = name
        self.price = price

    def __repr__(self):
        return '%s from %s' % (self.name, self.location)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courrier_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
        return 'Order %d @ %s' % (self.id, self.location.name)

    def group_by_user(self):
        group = defaultdict(list)
        for item in self.items:
            group[item.get_name()] += [item.product]
        return group

    def group_by_user_pay(self):
        group = defaultdict(int)
        for item in self.items:
            group[item.get_name()] += item.product.price
        return group

    def group_by_product(self):
        group = defaultdict(int)
        for item in self.items:
            group[item.product.name] += 1
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
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
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
        return 'Order %d: %s wants %s' % (self.order_id, self.get_name(), self.product.name)

    def can_delete(self, order_id, user_id, name):
        if int(self.order_id) != int(order_id):
            return False
        if self.order.stoptime and self.order.stoptime < datetime.now():
            return False
        if self.user_id == user_id or self.name == name:
            return True
        return False
