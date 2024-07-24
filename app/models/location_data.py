from dataclasses import dataclass
from .database import db

# This stores the data from the OpenStreetMap API for the locations
# This is used to extend the locations from the HLDS files later

@dataclass
class LocationData(db.Model):
    """Class used for configuring the LocationData model in the database"""
    osm_node_id = db.Column(db.String(32))
    hlds_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128))
    opening_hours = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    street = db.Column(db.String(128))
    housenumber = db.Column(db.String(32))
    website = db.Column(db.String(256))
