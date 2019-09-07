from app import db
from models import User


def add() -> None:
    feli = User()
    feli.configure("feliciaan", True, 0)
    db.session.add(feli)

    destro = User()
    destro.configure("destro", True, 0)
    db.session.add(destro)

    iepoev = User()
    iepoev.configure("iepoev", True, 1)
    db.session.add(iepoev)

    flynn = User()
    flynn.configure("flynn", True, 0)
    db.session.add(flynn)

    # To future developers, add yourself here
