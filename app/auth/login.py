"""Script for everything related to logging in and out"""
from flask import Blueprint, abort, redirect, session, url_for
from flask_login import current_user, logout_user
from ..models import User
from werkzeug.wrappers import Response

auth_bp = Blueprint("auth_bp", __name__)


def init_login(app) -> None:
    """Initialize the login"""

    # pylint: disable=W0612
    @app.login_manager.user_loader
    def load_user(userid) -> User:
        """Load the user"""
        return User.query.filter_by(id=userid).first()


@auth_bp.route("/logout")
def logout() -> Response:
    """Function to handle a user trying to log out"""
    if "zeus_token" in session:
        session.pop("zeus_token", None)
    logout_user()
    return redirect(url_for("general_bp.home"))


def before_request() -> None:
    """Function for what has to be done before a request"""
    if current_user.is_anonymous() or not current_user.is_allowed():
        abort(401)
