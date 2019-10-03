from app import db
from models import Location, Product

STUFFS = [
    ("Broodje zever", 540),
    ("Broodje aap", 0),
    ("Broodje goud", 500000),
]


def add() -> None:
    testlocation = Location()
    testlocation.configure(
        "Testlocation",
        "Please ignore!",
        "0469 69 69 69",
        "http://localhost:8000/",
    )
    db.session.add(testlocation)

    for stuff in STUFFS:
        entry = Product()
        entry.configure(testlocation, *stuff)
        db.session.add(entry)
