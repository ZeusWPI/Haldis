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

# To future developers, add yourself here

# commit all the things
db.session.commit()
