from models import Location, Product
from app import db

bickies = {
    "Bicky Burger Original": 330,
    "Bicky Burger": 300,
    "Bicky Glenniei": 330,
    "Bicky Capoentje": 330,
    "Bicky Chicken": 350,
    "Bicky Fish": 350,
    "Bicky Veggie": 350,
}

saus = {
    "american": 70,
    "andalouse": 70,
    "bicky saus": 70,
    "cocktail": 70,
    "curryketchu": 70,
    "gele curry saus": 70,
    "hannibal": 70,
    "jamballa": 70,
    "joppie": 70,
    "loempiasaus": 70,
    "looksaus": 70,
    "mammout saus": 70,
    "mayo": 70,
    "mosterd": 70,
    "pepersaus": 70,
    "pickles": 70,
    "pili-pili saus": 70,
    "samurai": 70,
    "tartare": 70,
    "ketchup": 70,
    "toscanse saus": 70,
    "zoete mayo": 70,
    "stoverijsaus": 130,
    "special op vlees": 80,
    "speciaal op friet": 160,
}

special_bickies = {
    "Bicky Yellow": 400,
    "Bicky Hermes": 500,
    "Bicky Grand Cru": 530,
    "Bicky Royal": 600,
    "Bicky Wrap": 400,
    "Bicky Rib": 450,
    "Lloydje/Plankske": 600,
}


specials = {
    "Julientje": 650,
    "Julientje Dubbel": 800,
    "Veggie Julientje": 700,
    "Veggie Julientje Dubbel": 800,
    "Rombautje": 700,
    "Rombautje Dubbel": 900,
    "Bolleke": 650,
    "Bolleke Dubbel": 800,
    "Hendrik": 700,
    "Hendrik Dubbel": 900,
    "Lieveke": 700,
    "Molleke": 850,
    "Molleke Dubbel": 1200,
    "Stefano": 650,
    "Stefano Dubbel": 800,
    "Picasso": 1350,
}

vlezekes = {
    "Ardeense sate": 350,
    "Bamischijf": 200,
    "5 Bitterballen": 150,
    "Jagerworst": 300,
    "Boulet": 200,
    "Chixfingers": 350,
    "Chicken Nuggets": 350,
    "Crizzly Pikant": 350,
    "Frikandel": 100,
    "Garnaalballetjes": 350,
    "Garnaalkroket": 300,
    "Kaasballetjes": 250,
    "Kaaskroket": 100,
    "Kipcorn": 200,
    "Kipsate": 400,
    "Loempia met kip": 350,
    "Lookworst": 300,
    "Merguez": 350,
    "Mexicano": 200,
    "Mini Loempia's met saus": 300,
    "Mini Lucifers": 300,
    "Ragouzi": 250,
    "stoofvlees": 450,
}

friet = {"Klein pak": 200, "Midden pak": 250, "Groot pak": 300}

data = [special_bickies, specials, vlezekes, friet]


def add():
    stefanos = Location()
    stefanos.configure(
        "Stefano's Place",
        "Overpoortstraat 12 9000 Gent",
        "tel: geen",
        "https://www.facebook.com/pages/category/Fast-Food-Restaurant/Stefanos-Place-370774480004139/",
    )
    db.session.add(stefanos)

    # sommige bickies kunde met een schel kaas bestellen
    for name, price in bickies.items():
        bicky = Product()
        bicky.configure(stefanos, name, price)
        db.session.add(bicky)

        bicky_cheese = Product()
        bicky_cheese.configure(stefanos, name + " cheese", price + 30)
        db.session.add(bicky_cheese)

    for dict in data:
        for name, price in dict.items():
            item = Product()
            item.configure(stefanos, name, price)
            db.session.add(item)

    # saus in een potteke bestellen is 10 cent extra
    for name, price in saus.items():
        saus = Product()
        saus.configure(stefanos, name, price)
        db.session.add(saus)

        saus_apart = Product()
        saus_apart.configure(stefanos, name + " apart", price + 10)
        db.session.add(saus_apart)
