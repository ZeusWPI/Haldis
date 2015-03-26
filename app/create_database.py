from models import *
from app import db

db.drop_all()
db.create_all()

feli = User()
feli.configure("feliciaan", True, True)
db.session.add(feli)

don = User()
don.configure("don", True, True)
db.session.add(don)

# To future developers, add yourself here

# commit all the things
db.session.commit()
