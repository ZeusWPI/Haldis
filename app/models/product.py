from models import db

from .location import Location


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orderItems = db.relationship("OrderItem",
                                 backref="product", lazy="dynamic")

    def configure(self, location: Location, name: str, price: int) -> None:
        self.location = location
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return "%s (€%d)from %s" % (
            self.name,
            self.price / 100,
            self.location or "None",
        )
