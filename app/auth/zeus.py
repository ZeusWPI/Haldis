"Script containing everything specific to ZeusWPI"
import typing

from flask import Blueprint, current_app, flash, redirect, request, session, url_for
from flask_login import login_user

# from flask_oauthlib.client import OAuth, OAuthException, OAuthRemoteApp
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import OAuthError
from ..models import User, db
from werkzeug.wrappers import Response

auth_zeus_bp = Blueprint("auth_zeus_bp", __name__)


def zeus_login():
    """Log in using ZeusWPI"""
    return current_app.zeus.authorize_redirect(
        url_for("auth_zeus_bp.authorized", _external=True)
    )


@auth_zeus_bp.route("/login")
def login():
    """Function to handle a user trying to log in"""
    return zeus_login()


@auth_zeus_bp.route("/authorized")
def authorized() -> typing.Any:
    # type is 'typing.Union[str, Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    """Check authorized status"""
    try:
        resp = current_app.zeus.authorize_access_token()
    except Exception as e:
        if isinstance(e, OAuthError):
            flash("Permission denied")
        else:
            flash(
                "An error occurred while logging in, please contact a system administrator"
            )
        return redirect(url_for("general_bp.home"))

    me = current_app.zeus.get("current_user")
    username = me.json().get("username", "").lower()

    user = User.query.filter_by(username=username).first()
    # pylint: disable=R1705
    if username and user:
        return login_and_redirect_user(user)
    elif username:
        user = create_user(username)
        return login_and_redirect_user(user)

    flash("You're not allowed to enter, please contact a system administrator")
    return redirect(url_for("general_bp.home"))


def init_oauth(app):
    """Initialize the OAuth for ZeusWPI"""
    oauth = OAuth(app)

    oauth.register(
        name="zeus",
        client_id=app.config["ZEUS_KEY"],
        client_secret=app.config["ZEUS_SECRET"],
        request_token_params={},
        api_base_url="https://zauth.zeus.gent/",
        access_token_method="POST",
        access_token_url="https://zauth.zeus.gent/oauth/token/",
        authorize_url="https://zauth.zeus.gent/oauth/authorize/",
    )

    return oauth.create_client("zeus")


def login_and_redirect_user(user) -> Response:
    """Log in the user and then redirect them"""
    login_user(user)
    return redirect(url_for("general_bp.home"))


def create_user(username) -> User:
    """Create a temporary user if it is needed"""
    user = User()
    user.configure(username, False, 1, associations=["zeus"])
    db.session.add(user)
    db.session.commit()
    return user
