from flask import current_app, flash, redirect, request, session, url_for, Blueprint
from flask_login import login_user
from flask_oauthlib.client import OAuthException, OAuth

from models import User, db

oauth_bp = Blueprint("oauth_bp", __name__)


def zeus_login():
    return current_app.zeus.authorize(
        callback=url_for("oauth_bp.authorized", _external=True)
    )


@oauth_bp.route("/login/zeus/authorized")
def authorized():
    resp = current_app.zeus.authorized_response()
    if resp is None:
        return "Access denied: reason=%s error=%s" % (
            request.args["error"],
            request.args["error_description"],
        )
    if isinstance(resp, OAuthException):
        return "Access denied: %s" % resp.message + "<br>" + str(resp.data)

    session["zeus_token"] = (resp["access_token"], "")
    me = current_app.zeus.get("current_user/")
    username = me.data.get("username", "").lower()

    user = User.query.filter_by(username=username).first()
    if len(username) > 0 and user:
        return login_and_redirect_user(user)
    elif len(username) > 0:
        user = create_user(username)
        return login_and_redirect_user(user)

    flash("You're not allowed to enter, please contact a system administrator")
    return redirect(url_for("general_bp.home"))


def init_oauth(app):
    oauth = OAuth(app)

    zeus = oauth.remote_app(
        "zeus",
        consumer_key=app.config["ZEUS_KEY"],
        consumer_secret=app.config["ZEUS_SECRET"],
        request_token_params={},
        base_url="https://adams.ugent.be/oauth/api/",
        access_token_method="POST",
        access_token_url="https://adams.ugent.be/oauth/oauth2/token/",
        authorize_url="https://adams.ugent.be/oauth/oauth2/authorize/",
    )

    @zeus.tokengetter
    def get_zeus_oauth_token():
        return session.get("zeus_token")

    return zeus


def login_and_redirect_user(user):
    login_user(user)
    return redirect(url_for("general_bp.home"))


def create_user(username):
    user = User()
    user.configure(username, False, 1)
    db.session.add(user)
    db.session.commit()
    return user
