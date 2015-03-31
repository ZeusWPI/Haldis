from models import *
from app import db
from itertools import product

db.drop_all()
db.create_all()

feli = User()
feli.configure("feliciaan", True, 0)
db.session.add(feli)

destro = User()
destro.configure('destro', True, 0)
db.session.add(destro)

iepoev = User()
iepoev.configure('iepoev', True, 1)
db.session.add(iepoev)

burrito = Location()
burrito.configure("Burrito Bar", "Top-4-straat Keknet-city", "burritofest.com")
db.session.add(burrito)

blauw_kotje = Location()
blauw_kotje.configure("'t Blauw Kotje", "Top-5-straat Keknet-city", "frietfest.com")
db.session.add(blauw_kotje)

chili_con_carne = Product()
chili_con_carne.configure(burrito, "Chili Con Carne", 550)
db.session.add(chili_con_carne)

medium_pak_frieten = Product()
medium_pak_frieten.configure(blauw_kotje, "Medium Pak Frieten", 220)
db.session.add(medium_pak_frieten)
# To future developers, add yourself here

############################################
#           Chinees autogenerate           #
############################################
zetmelen = ["Nasi", "Bami"]
vlezen = ["Rundsvlees", "Varkensvlees"]
sauzen = ["Balisaus", "Yu siang saus", "Gon boa saus", "Curry saus", "Oestersaus", "Zwarte pepersaus",
          "Champignons", "Chinese champignons", "A la Maleisïe"]
specials = ["Kippenbolletjes zoetzuur", "varkenbolletjes zoetzuur", "Nazi Babi Pangang", "Bami Babi Pangang",
           "Diverse groenten met bami(Vegetarisch)", "Diverse groenten met nazi(Vegetarisch)"]

chinees = Location()
chinees.configure("Oceans's Garden", "Top-4-straat Keknet-city", "http://oceangarden.byethost3.com/studentenmenus.html")
db.session.add(chinees)

def chinees_create_entry(zetmeel, vlees="", saus=""):
    entry = Product()
    entry.configure(chinees, "{} {} {}".format(zetmeel, vlees, saus).rstrip(), 550)
    db.session.add(entry)


for zetmeel, vlees, saus in product(zetmelen, vlezen, sauzen):
    chinees_create_entry(zetmeel, vlees, saus)

for special in specials:
    chinees_create_entry(special)
#############################################

# commit all the things
db.session.commit()
