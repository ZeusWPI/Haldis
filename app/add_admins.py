"""Script for adding users as admin to Haldis."""
from models import User

from app import db
from models import User
from config import Configuration


def add() -> None:
    """Add users as admin."""
    for username in Configuration.HALDIS_ADMINS:
        user = User()
        user.configure(username, True, 0)
        db.session.add(user)
