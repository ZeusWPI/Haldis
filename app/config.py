# config


class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///foodbot.db'
    DEBUG = True
    SECRET_KEY = '<change>'
    SLACK_WEBHOOK = ''
    PROCESS = 'python test.py'
    LOGFILE = 'slotmachien.log'
    ZEUS_KEY = 'tomtest'
    ZEUS_SECRET = 'blargh'
    SLACK_TOKEN = 'xoxp-2484654576-2486580711-4114448516-f21087'
