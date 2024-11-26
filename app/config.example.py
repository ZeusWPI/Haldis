"""An example for a Haldis config"""

import os


class Configuration:
    "Haldis configuration object"
    # pylint: disable=too-few-public-methods
    SQLALCHEMY_DATABASE_URI = "sqlite:///haldis.db"
    # MARIADB_HOST = os.environ.get("MARIADB_HOST")
    # MARIADB_DB = os.environ.get("MARIADB_DATABASE")
    # MARIADB_USER = os.environ.get("MARIADB_USER")
    # MARIADB_PASS = os.environ.get("MARIADB_PASSWORD")
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MARIADB_USER}:{MARIADB_PASS}@{MARIADB_HOST}/{MARIADB_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HALDIS_ADMINS = []
    SECRET_KEY = os.urandom(32) # Change this to a fixed, random value
    SLACK_WEBHOOK = None
    LOGFILE = "haldis.log"
    SENTRY_DSN = None
    ZEUS_KEY = "tomtest"
    ZEUS_SECRET = "blargh"
    REFRESH_OSM = False

    ENABLE_MICROSOFT_AUTH = False
    MICROSOFT_AUTH_ID = ""
    MICROSOFT_AUTH_SECRET = ""
