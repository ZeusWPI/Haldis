from models import db


class AttributeValues(db.Model):
    attribute_id = db.Column(db.Integer, db.ForeignKey('attribute.id'), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price_addition = db.Column(db.Integer, nullable=False)

    attribute = db.relationship("Attribute", back_populates="values")