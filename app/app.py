#!/usr/bin/env python3

"""Main Haldis script"""

import logging
import typing
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from admin import init_admin
from flask import Flask, render_template
from flask_bootstrap import Bootstrap, StaticCDN
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_oauthlib.client import OAuth, OAuthException
from flask_script import Manager, Server
from login import init_login
from markupsafe import Markup
from models import db
from models.anonymous_user import AnonymouseUser
from utils import euro_string, price_range_string
from zeus import init_oauth


def register_plugins(app: Flask) -> Manager:
    """Register the plugins to the app"""
    # pylint: disable=W0612
    if not app.debug:
        timedFileHandler = TimedRotatingFileHandler(
            app.config["LOGFILE"], when="midnight", backupCount=100
        )
        timedFileHandler.setLevel(logging.DEBUG)

        loglogger = logging.getLogger("werkzeug")
        loglogger.setLevel(logging.DEBUG)
        loglogger.addHandler(timedFileHandler)
        app.logger.addHandler(timedFileHandler)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    app_manager = Manager(app)
    app_manager.add_command("db", MigrateCommand)
    app_manager.add_command("runserver", Server(port=8000))
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

    # Make cookies more secure
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if not app.debug:
        app.config.update(SESSION_COOKIE_SECURE=True)

    return app_manager


def add_handlers(app: Flask) -> None:
    """Add handlers for 4xx error codes"""

    # pylint: disable=W0612,W0613
    @app.errorhandler(404)
    def handle404(e) -> typing.Tuple[str, int]:
        return render_template("errors/404.html"), 404

    @app.errorhandler(401)
    def handle401(e) -> typing.Tuple[str, int]:
        return render_template("errors/401.html"), 401


def add_routes(application: Flask) -> None:
    """Add all routes to Haldis"""
    # import views  # TODO convert to blueprint
    # import views.stats  # TODO convert to blueprint

    from login import auth_bp
    from views.debug import debug_bp
    from views.general import general_bp
    from views.order import order_bp
    from views.stats import stats_blueprint
    from zeus import oauth_bp

    application.register_blueprint(general_bp, url_prefix="/")
    application.register_blueprint(order_bp, url_prefix="/order")
    application.register_blueprint(stats_blueprint, url_prefix="/stats")
    application.register_blueprint(auth_bp, url_prefix="/")
    application.register_blueprint(oauth_bp, url_prefix="/")

    if application.debug:
        application.register_blueprint(debug_bp, url_prefix="/debug")


def add_template_filters(app: Flask) -> None:
    """Add functions which can be used in the templates"""

    # pylint: disable=W0612
    @app.template_filter("countdown")
    def countdown(
        value, only_positive: bool = True, show_text: bool = True, reload: bool = True
    ) -> str:
        delta = int(value.timestamp() - datetime.now().timestamp())
        if delta < 0 and only_positive:
            text = "closed"
        else:
            carry, seconds = divmod(delta, 60)
            carry, minutes = divmod(carry, 60)
            days, hours = divmod(carry, 24)

            days_text = f"{days} days, " if days else ""

            appendix = " left" if show_text else ""
            text = f"{days_text}{hours:02d}:{minutes:02d}:{seconds:02d}{appendix}"

        reload_str = "yes" if reload else "no"

        return Markup(
            f"<span class='time' data-seconds='{delta}' data-reload='{reload_str}'>"
            + text
            + "</span>"
        )

    @app.template_filter("year")
    def current_year(_value: typing.Any) -> str:
        return str(datetime.now().year)

    app.template_filter("euro")(euro_string)
    app.template_filter("price_range")(price_range_string)
    app.template_filter("any")(any)
    app.template_filter("all")(all)


def create_app():
    """Initializer for the Flask app object"""
    app = Flask(__name__)

    # Load the config file
    app.config.from_object("config.Configuration")

    app_manager = register_plugins(app)
    add_handlers(app)
    add_routes(app)
    add_template_filters(app)

    return app_manager


# For usage when you directly call the script with python
if __name__ == "__main__":
    app_mgr = create_app()
    app_mgr.run()
