import enum

from sqlalchemy import Enum

from models import db


class SelectionType(enum.Enum):
    single_select = 1
    multi_select = 2


class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    selection_type = db.Column(Enum(SelectionType))

    values = db.relationship("AttributeValues", back_populates="attribute")

    def configure(self, name: str, single_type: SelectionType):
        self.name = name
        self.single_type = single_type

    def __repr__(self):
        return '%s'.format(self.name)
