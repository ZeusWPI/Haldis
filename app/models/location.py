from models import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(254))
    website = db.Column(db.String(120))
    telephone = db.Column(db.String(20), nullable=True)
    products = db.relationship("Product", backref="location", lazy="dynamic")
    orders = db.relationship("Order", backref="location", lazy="dynamic")

    def configure(self, name, address, telephone, website):
        self.name = name
        self.address = address
        self.website = website
        self.telephone = telephone

    def __repr__(self):
        return "%s" % (self.name)
