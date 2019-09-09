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

    def configure(self, username: str, admin: bool, bias: int) -> None:
        self.username = username
        self.admin = admin
        self.bias = bias

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
