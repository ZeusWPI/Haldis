from app import db

# Create database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    runs = db.relationship('Order', backref='courrier', lazy='dynamic')
    orders = db.relationship('OrderItem', backref='user', lazy='dynamic')

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
    food = db.relationship('Food', backref='location', lazy='dynamic')

    def configure(self, name, address, website):
        self.name = name
        self.address = address
        self.website = website

    def __repr__(self):
        return '%s: %s' % (self.name, self.address)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    orders = db.relationship('OrderItem', backref='food', lazy='dynamic')


    def configure(self, location, name, price):
        self.location = location
        self.name = name
        self.price = price

    def __repr__(self):
        return '%s' % self.name


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courrier_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    orders = db.relationship('OrderItem', backref='order', lazy='dynamic')


    def configure(self, courrier, location, starttime, stoptime):
        self.courrier = courrier
        self.location = location
        self.starttime = starttime
        self.stoptime = stoptime

    def __repr__(self):
        return 'Order'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))

    def configure(self, user, order, food):
        self.user = user
        self.order = order
        self.food = food

    def __repr__(self):
        return 'OrderItem'
