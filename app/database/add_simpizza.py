from models import Location, Product
from app import db


pizzas = [
    "Bolognese de luxe",
    "Hawaï",
    "Popeye",
    "Pepperoni",
    "Seafood",
    "Hot pizzaaah!!!",
    "Salmon delight",
    "Full option",
    "Pitza kebab",
    "Multi cheese",
    "4 Seasons",
    "Mega fish",
    "Creamy multi cheese",
    "Green fiësta",
    "Chicken bbq",
    "Funky chicken",
    "Veggie",
    "Meat lovers" "Scampi mampi",
    "Tabasco",
    "Chicken time",
    "Meatballs",
    "Tuna",
    "Anchovy",
    "Calzone",
    "Bbq meatballs",
    "Creamy chicken",
    "Hot bolognese",
]


def add():
    simpizza = Location()
    simpizza.configure(
        "Sim-pizza",
        "De Pintelaan 252 9000 Gent",
        "tel: 09/321.02.00",
        "http://simpizza.be",
    )
    db.session.add(simpizza)

    for pizza in pizzas:
        entry = Product()
        entry.configure(simpizza, pizza, 1195)
        db.session.add(entry)
