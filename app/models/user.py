"Script for everything User related in the database"
from typing import List, Optional

from ..models import db


class User(db.Model):
    """Class used for configuring the User model in the database"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    admin = db.Column(db.Boolean)
    bias = db.Column(db.Integer)
    # Microsoft OAUTH info
    microsoft_uuid = db.Column(db.String(120), unique=True)
    # Association logic
    associations = db.Column(db.String(255), nullable=False, server_default="")

    # Relations
    runs = db.relation(
        "Order",
        backref="courier",
        primaryjoin="Order.courier_id==User.id",
        foreign_keys="Order.courier_id",
    )
    orderItems = db.relationship("OrderItem", backref="user", lazy="dynamic")

    def association_list(self) -> List[str]:
        return self.associations.split(",")

    def configure(self, username: str, admin: bool, bias: int, *, microsoft_uuid: str = None, associations: Optional[List[str]] = None) -> None:
        """Configure the User"""
        if associations is None:
            associations = []
        self.username = username
        self.admin = admin
        self.bias = bias
        self.microsoft_uuid = microsoft_uuid
        self.associations = ",".join(associations)

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
        return f"{self.username}"
