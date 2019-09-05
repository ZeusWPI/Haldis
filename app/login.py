from flask import abort, Blueprint
from flask import redirect, session, url_for
from flask_login import current_user, logout_user

from models import User
from zeus import zeus_login

auth_bp = Blueprint("auth_bp", __name__)


def init_login(app):
    @app.login_manager.user_loader
    def load_user(userid):
        return User.query.filter_by(id=userid).first()


@auth_bp.route("/login")
def login():
    return zeus_login()


@auth_bp.route("/logout")
def logout():
    if "zeus_token" in session:
        session.pop("zeus_token", None)
    logout_user()
    return redirect(url_for("general_bp.home"))


def before_request():
    if current_user.is_anonymous() or not current_user.is_allowed():
        abort(401)
