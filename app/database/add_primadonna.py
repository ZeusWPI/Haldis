from models import Location, Product
from app import db

pizzasTA = {"Peperoni":750, "Basis pizza (extra garneringen zie site)":600, "Parma":750, "Margharita": 600, "Funghi":715, "Mamma mia":715, "Napoletana":750, "Exotic":750, "Siciliana":750, "Michelangelo":750, "Roma":750, "Torno":750, "Bolognese":780, "Hawai":910, "Cipolla":910, "Dolce vita":910, "Valentino":910, "Vegateriana":1000, "La donna":1000, "Tropical":1000, "Quattro Stagioni":1000, "Romana":1000, "Diabolo":1000, "Turkish":1000, "Cesar":1000, "Calzone":1040, "Calzone Vegetariana":1040, "Quattro Formaggi":1040, "Frutti di mare":1040, "Gerookte ham en rucola":1040, "Van de chef":1170, "Milano":1170, "Soronto":1260, "Primma Donna":1260, "Pasta (zie site voor opties)":900}


def addTA():
    primadonna_takeaway = Location()
    primadonna_takeaway.configure("Primadonna takeaway.com", "Overpoortstraat 46 9000 Gent, tel: 0475 40 13 00", "https://www.takeaway.com/be-en/prima-donna")
    db.session.add(primadonna_takeaway)

    for pizza in pizzaTA.keys:
        entry = Product()
        entry.configure(primadonna_takeaway, pizza, pizzasTA.get(pizza, 0))
        db.session.add(entry)
