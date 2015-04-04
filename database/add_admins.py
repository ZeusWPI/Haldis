from app import db
from models import User


def add():
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