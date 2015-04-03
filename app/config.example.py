# config

class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///haldis.db'
    DEBUG = True
    SECRET_KEY = '<change>'
    SLACK_WEBHOOK = '<add url>'
    LOGFILE = 'haldis.log'
    ZEUS_KEY = ''
    ZEUS_SECRET = ''
