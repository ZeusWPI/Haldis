from models import Location, Product
from app import db


menuitems = [
    "Spicy Chicken",
    "Advocado Chick",
    "Indian Summer",
    "Olive Garden",
    "Advocado Spring",
    "Spicy Mexican",
    "Beefcake",
    "Iron Man",
    "Fitalian",
    "Captain",
    "Sea Breeze",
    "Vegan Market",
    "Sunset Beach",
    "Hot Tofu",
    "Vegan Advocado Spring",
]

pricedict = {"Small": 799, "Medium": 999, "Large": 1199}


def add():
    simpizza = Location()
    simpizza.configure("Fitchen", "?", "?", "https://www.fitchen.be/")
    db.session.add(simpizza)

    for menuitem in menuitems:
        for size, price in pricedict.items():
            for container in ["bowl", "wrap"]:
                name = "%s %s in %s" % (size, menuitem, container)
                entry = Product()
                entry.configure(simpizza, name, price)
                db.session.add(entry)
