import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask.ext.bootstrap import Bootstrap, StaticCDN
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.Configuration')
Bootstrap(app)

# use our own bootstrap theme
app.extensions['bootstrap']['cdns']['bootstrap'] = StaticCDN()

db = SQLAlchemy(app)

class PrefixFix(object):

    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        path = environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', '')
        environ['SCRIPT_NAME'] = self.script_name
        environ['PATH_INFO'] = path[len(self.script_name):]
        return self.app(environ, start_response)


if not app.debug:
    app.wsgi_app = PrefixFix(app.wsgi_app, '/james')
    timedFileHandler = TimedRotatingFileHandler(app.config['LOGFILE'], when='midnight', backupCount=100)
    timedFileHandler.setLevel(logging.INFO)
    logger = logging.getLogger('werkzeug')
    logger.addHandler(timedFileHandler)
    app.logger.addHandler(timedFileHandler)

