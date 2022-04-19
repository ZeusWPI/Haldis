"""Script for adding users as admin to Haldis."""
from models import User

from app import db


def add() -> None:
    """Add users as admin."""
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
