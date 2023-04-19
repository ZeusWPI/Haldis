"""An example for a Haldis config"""
# config


class Configuration:
    "Haldis configuration object"
    # pylint: disable=too-few-public-methods
    SQLALCHEMY_DATABASE_URI = "sqlite:///haldis.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HALDIS_ADMINS = []
    SECRET_KEY = "<change>"
    SLACK_WEBHOOK = None
    LOGFILE = "haldis.log"
    SENTRY_DSN = None
    ZEUS_KEY = "tomtest"
    ZEUS_SECRET = "blargh"

    ENABLE_MICROSOFT_AUTH = False
    MICROSOFT_AUTH_ID = ""
    MICROSOFT_AUTH_SECRET = ""
