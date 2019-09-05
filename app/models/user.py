from models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    runs = db.relation(
        "Order",
        backref="courrier",
        primaryjoin="Order.courrier_id==User.id",
        foreign_keys="Order.courrier_id",
    )
    orderItems = db.relationship("OrderItem", backref="user", lazy="dynamic")

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
        return str(self.id)

    def __repr__(self):
        return "%s" % self.username
