from flask import Flask
from flask.ext.bootstrap import Bootstrap, StaticCDN
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.Configuration')
Bootstrap(app)

# use our own bootstrap theme
app.extensions['bootstrap']['cdns']['bootstrap'] = StaticCDN()

db = SQLAlchemy(app)

