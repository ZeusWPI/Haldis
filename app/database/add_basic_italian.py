"Script to add Basic Italian I to Haldis"
from app import db
from models import Location, Product

menuitems = [
    "Pomodoro",
    "Pesto",
    "Mascarpone",
    "Spinaci",
    "Carbonara",
    "Quatro fromaggi",
    "Arrabiata",
    "Diabolique",
    "Bolognaise",
]

pricedict = {"Small": 700, "Medium": 900, "Large": 1100}


def add() -> None:
    "Add Basic Italian I to the database"
    basic_italian = Location()
    basic_italian.configure(
            "Basic Italian I",
            "Sint-Pietersplein 42 9000 Gent",
            "gsm: +32475/25.84.89",
            "https://www.takeaway.com/be-en/basic-italian-i",
    )
    db.session.add(basic_italian)

    for menuitem in menuitems:
        for size, price in pricedict.items():
            name = "%s %s in %s" % (size, menuitem, 'pasta')
            entry = Product()
            entry.configure(basic_italian, name, price)
            db.session.add(entry)
