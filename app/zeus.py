from flask import Flask, redirect, url_for, session, request, jsonify, flash, request
from flask.ext.login import LoginManager, login_user, current_user, logout_user
from flask.ext.admin import helpers
from flask_oauthlib.client import OAuth, OAuthException
import json
import requests


from app import app, db
from models import User, Token

oauth = OAuth(app)

zeus = oauth.remote_app(
    'zeus',
    consumer_key=app.config['ZEUS_KEY'],
    consumer_secret=app.config['ZEUS_SECRET'],
    request_token_params={},
    base_url='http://kelder.zeus.ugent.be/oauth/api/',
    access_token_method='POST',
    access_token_url='https://kelder.zeus.ugent.be/oauth/oauth2/token/',
    authorize_url='https://kelder.zeus.ugent.be/oauth/oauth2/authorize/'
)


def zeus_login():
    if app.debug:
        return zeus.authorize(callback=url_for('authorized', _external=True))
    else: # temporary solution because it otherwise gives trouble on the pi because of proxies and such
        return zeus.authorize(callback='http://zeus.ugent.be/foodbot/login/zeus/authorized')


@app.route('/slotmachien/login/zeus/authorized')
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
    return redirect(url_for("admin.index"))


@zeus.tokengetter
def get_zeus_oauth_token():
    return session.get('zeus_token')


def login_and_redirect_user(user):
    login_user(user)
    # add_token(resp['access_token'], user)
    content_type = request.headers.get('Content-Type', None)
    if content_type and content_type in 'application/json':
        token = add_token(user)
        return jsonify({'token': token.token})
    return redirect(url_for("admin.index"))


def add_token(user):
    token = Token()
    token.configure(user)
    db.session.add(token)
    db.session.commit()
    return token


def create_user(username):
    user = User()
    user.configure(username, False)
    db.session.add(user)
    db.session.commit()
    # EASTER EGG
    text = 'Welcome ' + username + '!'
    js = json.dumps({'text': text})
    url = app.config['SLACK_WEBHOOK']
    if len(url) > 0:
        requests.post(url, data=js)
    return user
