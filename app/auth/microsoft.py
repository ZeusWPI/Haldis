import typing

from flask import Blueprint, url_for, request, redirect, flash, Response
from flask_login import login_user
from microsoftgraph.client import Client

from config import Configuration
from models import User, db

auth_microsoft_bp = Blueprint("auth_microsoft_bp", __name__)

client = Client(Configuration.MICROSOFT_AUTH_ID,
                Configuration.MICROSOFT_AUTH_SECRET,
                account_type='common')  # by default common, thus account_type is optional parameter.


def microsoft_login():
    """Log in using Microsoft"""
    scope = ["openid", "profile", "User.Read", "User.Read.All"]
    url = client.authorization_url(url_for("auth_microsoft_bp.authorized", _external=True), scope, state=None)
    return redirect(url)


@auth_microsoft_bp.route("/login")
def login():
    """Function to handle a user trying to log in"""
    return microsoft_login()


@auth_microsoft_bp.route("callback")  # "/authorized")
def authorized() -> typing.Any:
    # type is 'typing.Union[str, Response]', but this errors due to
    #   https://github.com/python/mypy/issues/7187
    """Check authorized status"""

    oauth_code = request.args['code']

    resp = client.exchange_code(url_for("auth_microsoft_bp.authorized", _external=True), oauth_code)
    client.set_token(resp.data)

    resp = client.users.get_me()
    username = resp.data['userPrincipalName']
    microsoft_uuid = resp.data['id']

    user = User.query.filter_by(username=username).first()
    if username and user:
        return login_and_redirect_user(user)
    elif username:
        user = create_user(username, microsoft_uuid)
        return login_and_redirect_user(user)

    flash("You're not allowed to enter, please contact a system administrator")
    return redirect(url_for("general_bp.home"))


def login_and_redirect_user(user) -> Response:
    """Log in the user and then redirect them"""
    login_user(user)
    return redirect(url_for("general_bp.home"))


def create_user(username, microsoft_uuid) -> User:
    """Create a temporary user if it is needed"""
    user = User()
    user.configure(username, False, 1, microsoft_uuid=microsoft_uuid)
    db.session.add(user)
    db.session.commit()
    return user
