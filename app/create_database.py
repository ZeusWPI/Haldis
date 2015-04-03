from models import *
from app import db
from itertools import product


def recreate_db():
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


def add_chinees():
    chinees = Location()
    chinees.configure("Oceans's Garden", "Zwijnaardsesteenweg 399 9000 Gent, tel: 09/222.72.74", "http://oceangarden.byethost3.com/studentenmenus.html")
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

############################################
#           Simpizza autogenerate           #
############################################
pizzas = ['Bolognese de luxe', 'Hawaï', 'Popeye', 'Pepperoni', 'Seafood', 'Hot pizzaaah!!!', 'Salmon delight',
          'Full option', 'Pitza kebab', 'Multi cheese', '4 Seasons', 'Mega fish', 'Creamy multi cheese',
          'Green fiësta', 'Chicken bbq', 'Funky chicken', 'Veggie', 'Meat lovers', 'Scampi mampi', 'Tabasco',
          'Chicken time', 'Meatballs', 'Tuna', 'Anchovy', 'Calzone', 'Bbq meatballs', 'Creamy chicken', 'Hot bolognese']


def add_simpizza():
    simpizza = Location()
    simpizza.configure("Sim-pizza", "De Pintelaan 252 9000 Gent, tel: 09/321.02.00", "http://simpizza.be")
    db.session.add(simpizza)

    for pizza in pizzas:
        entry = Product()
        entry.configure(simpizza, pizza, 1195)
        db.session.add(entry)


def commit():
    # commit all the things
    db.session.commit()
    print("Committing successful")

locations = {'Ocean\'s Garden': add_chinees, 'Sim-pizza': add_simpizza}

print('Create database script!')
print('=======================\n\n')

db_key = 'recreate this database now!'
input_db = input("To recreate the db type: '" + db_key + "'")
if db_key in input_db:
    print("recreating the database!")
    recreate_db()
    for location in locations.values():
        location()
    commit()
else:
    print("not recreating the database!")
    # DID NOT RECREATE ASK IF YOU WANT TO RECREATE THE NEXT ONES
    for name, function in locations.items():
        add_location = input("Do you want to add " + name + "? Press: 'Y'")
        print("Adding " + name)
        if add_location.lower() in ['y', 'yes']:
            function()
    commit()