# config


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///haldis.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = "<change>"
    SLACK_WEBHOOK = "<add url>"
    LOGFILE = "haldis.log"
    ZEUS_KEY = "tomtest"
    ZEUS_SECRET = "blargh"
    AIRBRAKE_ID = ""
    AIRBRAKE_KEY = ""
