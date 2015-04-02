from views import *

from app import app, db

from admin import admin
from login import login_manager
from models import *
from forms import *
from utils import *
from views import *

if __name__ == '__main__':
	if app.debug:
		app.run(host='0.0.0.0', port=80)
	else:
		app.run()
