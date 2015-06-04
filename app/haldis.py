from views import *

from app import app, db

from admin import admin
from login import login_manager
from models import *
from forms import *
from utils import *
from views import *
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

if __name__ == '__main__':
    # do it here, because make accessing db changes only possible when executing the program directly
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
