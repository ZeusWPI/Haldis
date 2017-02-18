from flask import redirect, url_for, session, jsonify, flash, request
from flask_login import login_user
from flask_oauthlib.client import OAuth, OAuthException
import json
import requests


from app import app, db
from models import User

oauth = OAuth(app)

zeus = oauth.remote_app(
    'zeus',
    consumer_key=app.config['ZEUS_KEY'],
    consumer_secret=app.config['ZEUS_SECRET'],
    request_token_params={},
    base_url='https://adams.ugent.be/oauth/api/',
    access_token_method='POST',
    access_token_url='https://adams.ugent.be/oauth/oauth2/token/',
    authorize_url='https://adams.ugent.be/oauth/oauth2/authorize/'
)


def zeus_login():
    return zeus.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/zeus/authorized')
def authorized():
    resp = zeus.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message + '<br>' + str(resp.data)

    session['zeus_token'] = (resp['access_token'], '')
    me = zeus.get('current_user/')
    username = me.data.get('username', '').lower()

    user = User.query.filter_by(username=username).first()
    if len(username) > 0 and user:
        return login_and_redirect_user(user)
    elif len(username) > 0:
        user = create_user(username)
        return login_and_redirect_user(user)

    flash("You're not allowed to enter, please contact a system administrator")
    return redirect(url_for("home"))


@zeus.tokengetter
def get_zeus_oauth_token():
    return session.get('zeus_token')


def login_and_redirect_user(user):
    login_user(user)
    return redirect(url_for("home"))


def create_user(username):
    user = User()
    user.configure(username, False, 1)
    db.session.add(user)
    db.session.commit()
    return user
