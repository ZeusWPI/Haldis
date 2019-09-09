"Script to add Ocean Garden to Haldis"
from itertools import product

from app import db
from models import Location, Product

zetmelen = ["Nasi", "Bami"]
vlezen = ["Rundsvlees", "Varkensvlees", "Kippenstukkjes"]
sauzen = [
    "Balisaus",
    "Yu siang saus",
    "Gon boa saus",
    "Curry saus",
    "Oestersaus",
    "Zwarte pepersaus",
    "Champignons",
    "Chinese champignons",
    "A la Maleisïe",
]

specials = [
    "Nasi Kippenbolletjes Zoetzuur",
    "Bami Kippenbolletjes Zoetzuur",
    "Nasi Varkenbolletjes Zoetzuur",
    "Bami Varkenbolletjes Zoetzuur",
    "Nasi Babi Pangang",
    "Bami Babi Pangang",
    "Diverse Groenten met Bami",
    "Diverse Groenten met Nasi",
]


def add() -> None:
    "Add Ocean Garden to the database"
    chinees = Location()
    chinees.configure(
        "Oceans's Garden",
        "Zwijnaardsesteenweg 399 9000 Gent",
        "tel: 09/222.72.74",
        "http://oceangarden.byethost3.com/studentenmenus.html",
    )
    db.session.add(chinees)

    def chinees_create_entry(name) -> None:
        entry = Product()
        entry.configure(chinees, name, 550)
        db.session.add(entry)

    def chinees_create_regulat(zetmeel, vlees="", saus="") -> None:
        chinees_create_entry("{} {} {}".format(zetmeel, vlees, saus).rstrip())

    for z, v, s in product(zetmelen, vlezen, sauzen):
        chinees_create_regulat(z, v, s)

    for special in specials:
        chinees_create_entry(special)
