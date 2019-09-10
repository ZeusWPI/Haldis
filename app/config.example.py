"An example for a Haldis config"
# config


class Configuration():
    "Haldis configuration object"
    # pylint: disable=R0903
    SQLALCHEMY_DATABASE_URI = "sqlite:///haldis.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = "<change>"
    SLACK_WEBHOOK = None
    LOGFILE = "haldis.log"
    ZEUS_KEY = "tomtest"
    ZEUS_SECRET = "blargh"
    AIRBRAKE_ID = ""
    AIRBRAKE_KEY = ""
