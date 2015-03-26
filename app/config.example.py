# config


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///foodbot.db'
    DEBUG = True
    SECRET_KEY = '<change>'
    SLACK_WEBHOOK = '<add url>'
    LOGFILE = 'foodbot.log'
    ZEUS_KEY = ''
    ZEUS_SECRET = ''
