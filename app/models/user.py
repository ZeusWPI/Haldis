"Script for everything User related in the database"
from models import db


class User(db.Model):
    "Class used for configuring the User model in the database"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    runs = db.relation(
        "Order",
        backref="courier",
        primaryjoin="Order.courier_id==User.id",
        foreign_keys="Order.courier_id",
    )
    orderItems = db.relationship("OrderItem", backref="user", lazy="dynamic")

    def configure(self, username: str, admin: bool, bias: int) -> None:
        "Configure the User"
        self.username = username
        self.admin = admin
        self.bias = bias

    # pylint: disable=C0111, R0201
    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_admin(self) -> bool:
        return self.admin

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return "%s" % self.username
