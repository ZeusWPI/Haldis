from models import db

product_attribute_association_table = db.Table(
    "product_attribute_association_table",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("attribute_id", db.Integer, db.ForeignKey("attribute.id")),
)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    name = db.Column(db.String(120), nullable=False)
    base_price = db.Column(
        db.Integer, nullable=False
    )  # , server_default='0', default=0)
    orderItems = db.relationship("OrderItem", backref="Product", lazy="dynamic")
    comment = db.Column(db.String(255), nullable=True)
    attributes = db.relationship(
        "Attribute", secondary=product_attribute_association_table, backref="Product"
    )

    def configure(self, location, name, price):
        self.location = location
        self.name = name
        self.price = price

    def __repr__(self):
        return "%s (€%d)from %s".format(
            self.name, self.price / 100, self.location or "None"
        )
