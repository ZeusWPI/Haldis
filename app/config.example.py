# config

class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///james.db'
    DEBUG = True
    SECRET_KEY = '<change>'
    SLACK_WEBHOOK = '<add url>'
    LOGFILE = 'james.log'
    ZEUS_KEY = ''
    ZEUS_SECRET = ''
