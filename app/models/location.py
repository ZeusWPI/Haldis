from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models import db


class Location(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    address = Column(String(254))
    website = Column(String(120))
    telephone = Column(String(20), nullable=True)

    products = relationship("Product", backref="location", lazy="dynamic")
    orders = relationship("Order", backref="location", lazy="dynamic")

    def configure(self, name, address, telephone, website):
        self.name = name
        self.address = address
        self.website = website
        self.telephone = telephone

    def __repr__(self):
        return "%s".format(self.name)
