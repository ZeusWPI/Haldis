"""Script for adding users as admin to Haldis."""

from app.app import db
from app.models import User
from app.config import Configuration


def add() -> None:
    """Add users as admin."""
    for username in Configuration.HALDIS_ADMINS:
        user = User()
        user.configure(username, True, 0, associations=["zeus"])
        db.session.add(user)
