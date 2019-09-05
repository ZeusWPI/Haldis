import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from airbrake import Airbrake, AirbrakeHandler
from flask import Flask, render_template
from flask_bootstrap import Bootstrap, StaticCDN
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_oauthlib.client import OAuth, OAuthException
from flask_script import Manager, Server

from admin import init_admin
from login import init_login
from models import db
from models.anonymous_user import AnonymouseUser
from utils import euro_string
from zeus import init_oauth


def create_app():
    app = Flask(__name__)

    # Load the config file
    app.config.from_object("config.Configuration")

    manager = register_plugins(app, debug=app.debug)
    add_handlers(app)
    add_routes(app)
    add_template_filters(app)

    # TODO do we need to return and then run the manager?
    return manager


def register_plugins(app, debug: bool):
    # Register Airbrake and enable the logrotation
    if not app.debug:
        timedFileHandler = TimedRotatingFileHandler(
            app.config["LOGFILE"], when="midnight", backupCount=100
        )
        timedFileHandler.setLevel(logging.DEBUG)

        loglogger = logging.getLogger("werkzeug")
        loglogger.setLevel(logging.DEBUG)
        loglogger.addHandler(timedFileHandler)
        app.logger.addHandler(timedFileHandler)

        airbrakelogger = logging.getLogger("airbrake")

        # Airbrake
        airbrake = Airbrake(
            project_id=app.config["AIRBRAKE_ID"], api_key=app.config["AIRBRAKE_KEY"]
        )
        # ugly hack to make this work for out errbit
        airbrake._api_url = "http://errbit.awesomepeople.tv/api/v3/projects/{}/notices".format(
            airbrake.project_id
        )

        airbrakelogger.addHandler(AirbrakeHandler(airbrake=airbrake))
        app.logger.addHandler(AirbrakeHandler(airbrake=airbrake))

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    manager.add_command("runserver", Server(port=8000))

    # Add admin interface
    init_admin(app, db)

    # Init login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.anonymous_user = AnonymouseUser
    init_login(app)

    # Add oauth
    zeus = init_oauth(app)
    app.zeus = zeus

    # Load the bootstrap local cdn
    Bootstrap(app)
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True

    # use our own bootstrap theme
    app.extensions["bootstrap"]["cdns"]["bootstrap"] = StaticCDN()

    # Load the flask debug toolbar
    toolbar = DebugToolbarExtension(app)

    return manager


def add_handlers(app):
    @app.errorhandler(404)
    def handle404(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(401)
    def handle401(e):
        return render_template("errors/401.html"), 401


def add_routes(application):
    # import views  # TODO convert to blueprint
    # import views.stats  # TODO convert to blueprint

    from views.order import order_bp
    from views.general import general_bp
    from views.stats import stats_blueprint
    from views.debug import debug_bp
    from login import auth_bp
    from zeus import oauth_bp

    application.register_blueprint(general_bp, url_prefix="/")
    application.register_blueprint(order_bp, url_prefix="/order")
    application.register_blueprint(stats_blueprint, url_prefix="/stats")
    application.register_blueprint(auth_bp, url_prefix="/")
    application.register_blueprint(oauth_bp, url_prefix="/")

    if application.debug:
        application.register_blueprint(debug_bp, url_prefix="/debug")


def add_template_filters(app):
    @app.template_filter("countdown")
    def countdown(value, only_positive=True, show_text=True):
        delta = value - datetime.now()
        if delta.total_seconds() < 0 and only_positive:
            return "closed"
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time = "%02d:%02d:%02d" % (hours, minutes, seconds)
        if show_text:
            return "closes in " + time
        return time

    @app.template_filter("year")
    def current_year(value):
        return str(datetime.now().year)

    @app.template_filter("euro")
    def euro(value):
        euro_string(value)


# For usage when you directly call the script with python
if __name__ == "__main__":
    manager = create_app()
    manager.run()
