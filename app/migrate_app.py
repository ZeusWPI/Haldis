from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.config import Configuration

app = Flask(__name__)


config = Configuration()
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)