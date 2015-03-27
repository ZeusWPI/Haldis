from flask import redirect, abort, session, url_for
from flask.ext.login import LoginManager, current_user, logout_user


from app import app
from models import User
from zeus import zeus_login

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@app.route('/login')
def login():
    return zeus_login()


@app.route('/logout')
def logout():
    if 'zeus_token' in session:
        session.pop('zeus_token', None)
    logout_user()
    return redirect(url_for('home'))


def before_request():
    if current_user.is_anonymous() or not current_user.is_allowed():
        abort(401)
