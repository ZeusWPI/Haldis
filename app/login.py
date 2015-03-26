from flask import redirect, request, url_for, abort, session
from flask.ext.login import LoginManager, current_user, logout_user
from flask_oauthlib.client import OAuth

import requests

from app import app, db, logger, cache
from models import User
from zeus import oauth, zeus_login

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@app.route('/foodbot/login')
def login():
    return zeus_login()


@app.route('/foodbot/logout')
def logout():
    if 'zeus_token' in session:
        session.pop('zeus_token', None)
    logout_user()
    return redirect(url_for('admin.index'))


def before_request():
    if current_user.is_anonymous() or not current_user.is_allowed():
        abort(401)
