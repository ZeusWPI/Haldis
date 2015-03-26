from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache


from logbook import Logger

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = SQLAlchemy(app)
