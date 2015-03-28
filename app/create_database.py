from models import *
from app import db

db.drop_all()
db.create_all()

feli = User()
feli.configure("feliciaan", True, 0)
db.session.add(feli)

destro = User()
destro.configure('wout', True, 0)
db.session.add(destro)

burrito = Location()
burrito.configure("Burrito Bar", "Top-4-straat Keknet-city", "burritofest.com")
db.session.add(burrito)

blauw_kotje = Location()
blauw_kotje.configure("'t Blauw Kotje", "Top-5-straat Keknet-city", "frietfest.com")
db.session.add(blauw_kotje)

chili_con_carne = Food()
chili_con_carne.configure(burrito, "Chili Con Carne", 550)
db.session.add(chili_con_carne)

medium_pak_frieten = Food()
medium_pak_frieten.configure(blauw_kotje, "Medium Pak Frieten", 220)
db.session.add(medium_pak_frieten)
# To future developers, add yourself here

# commit all the things
db.session.commit()
