from requests import get
from app.hlds.models import Location
from app.models.location_data import LocationData
from app.models import db

from urllib.parse import urlparse
import os
def extend_locations(app, hlds_locations: list[Location]) -> list[Location]:
    """
    Extend the HLDS locations with the OSM data
    Update OSM data if it exists, otherwise add it
    """
    with app.app_context():
        existing_data: list[LocationData] = LocationData.query.all()
        # force refresh data
        if os.environ.get("REFRESH_OSM") == "true":
            for location in hlds_locations:
                get_data_and_update(location)
        # only get missing data
        else:
            for location in hlds_locations:
                for data in existing_data:
                    # data exists in the db
                    if location.id == data.hlds_id:
                        location = update_location(location, data)
                        break
                # get data from osm
                else:
                    get_data_and_update(location)
    hlds_locations.sort(key=lambda l: l.name)
    return hlds_locations

def get_data_and_update(location: Location):
    if not location.osm:
        return

    path = urlparse(location.osm).path
    location_data = get_data_from_osm_node(path)
    location_data.hlds_id = location.id
    db_location_data: LocationData | None = LocationData.query.filter_by(hlds_id=location.id).first()
    if db_location_data:
        db_location_data.housenumber = location_data.housenumber
        db_location_data.name = location_data.name
        db_location_data.opening_hours = location_data.opening_hours
        db_location_data.phone = location_data.phone
        db_location_data.street = location_data.street
        db_location_data.website = location_data.website
    else:
        db.session.add(location_data)
    db.session.commit()
    
    location = update_location(location, location_data)


def get_data_from_osm_node(path: str) -> LocationData:
    print(f"https://api.openstreetmap.org/api/0.6{path}")
    resp = get(f"https://api.openstreetmap.org/api/0.6{path}", headers={'Accept': 'application/json'})
    if resp.status_code == 200:
        element = resp.json().get("elements", [{}])[0]
        node_id = element.get("id")
        tags: dict = element.get("tags", {})

        location_data = LocationData()
        location_data.osm_node_id = node_id
        location_data.name = tags.get("name", "")
        location_data.opening_hours = tags.get("opening_hours", "")
        location_data.phone = tags.get("phone", "")
        location_data.street = tags.get("addr:street", "")
        location_data.housenumber = tags.get("addr:housenumber", "")
        location_data.website = tags.get("website", tags.get("contact:website", ""))

        return location_data
    else:
        print(f"Error fetching data from OSM: {resp.status_code}")
        return LocationData()


def update_location(location: Location, location_data: LocationData) -> Location:
    if location_data.phone: location.telephone = location_data.phone
    if location_data.website: location.website = location_data.website
    if location_data.opening_hours: location.opening_hours = location_data.opening_hours

    return location