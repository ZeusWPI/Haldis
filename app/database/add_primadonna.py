from models import Location, Product
from app import db

def add():
    addTA()
    addAfhalen()

pizzasTA = {
        "Peperoni":750,
        "Basis pizza (extra garneringen zie site)":600,
        "Parma":750,
        "Margharita":600,
        "Funghi":715,
        "Mamma mia":715,
        "Napoletana":750,
        "Exotic":750,
        "Siciliana":750,
        "Michelangelo":750,
        "Roma":750,
        "Torno":750,
        "Bolognese":780,
        "Hawai":910,
        "Cipolla":910,
        "Dolce vita":910,
        "Valentino":910,
        "Vegateriana":1000,
        "La donna":1000,
        "Tropical":1000,
        "Quattro Stagioni":1000,
        "Romana":1000,
        "Diabolo":1000,
        "Turkish":1000,
        "Cesar":1000,
        "Calzone":1040,
        "Calzone Vegetariana":1040,
        "Quattro Formaggi":1040,
        "Frutti di mare":1040,
        "Gerookte ham en rucola":1040,
        "Van de chef":1170,
        "Milano":1170,
        "Soronto":1260,
        "Primma Donna":1260,
        "Pasta (zie site voor opties)":900
        }

def addTA():
    primadonna_takeaway = Location()
    primadonna_takeaway.configure("Primadonna (takeaway laten bezorgen)", "Overpoortstraat 46 9000 Gent, tel: 0475 40 13 00", "https://www.takeaway.com/be-en/prima-donna")
    db.session.add(primadonna_takeaway)

    for pizza, price in pizzasTA.items():
        entry = Product()
        entry.configure(primadonna_takeaway, pizza, price)
        db.session.add(entry)

pizzasAfhalen = {
        "Peperoni":575,
        "Basis pizza (extra garneringen zie site)":450,
        "Parma":575,
        "Margharita":450,
        "Funghi":550,
        "Mamma mia":550,
        "Napoletana":575,
        "Exotic":575,
        "Siciliana":575,
        "Michelangelo":575,
        "Roma":575,
        "Torno":575,
        "Bolognese":600,
        "Hawai":700,
        "Cipolla":700,
        "Dolce vita":700,
        "Valentino":700,
        "Vegateriana":770,
        "La donna":770,
        "Tropical":770,
        "Quattro Stagioni":770,
        "Romana":770,
        "Diabolo":770,
        "Turkish":770,
        "Cesar":770,
        "Calzone":800,
        "Calzone Vegetariana":800,
        "Quattro Formaggi":800,
        "Frutti di mare":800,
        "Gerookte ham en rucola":800,
        "Van de chef":900,
        "Milano":900,
        "Soronto":970,
        "Primma Donna":970,
        "Pasta (zie site voor opties)":700
        }

def addAfhalen():
    primadonna_afhalen = Location()
    primadonna_afhalen.configure("Primadonna (bellen en afhalen)", "Overpoortstraat 46 9000 Gent, tel: 0475 40 13 00", "http://primadonnagent.be/Menu.html")
    db.session.add(primadonna_afhalen)

    for pizza, price in pizzasAfhalen.items():
        entry = Product()
        entry.configure(primadonna_afhalen, pizza, price)
        db.session.add(entry)

