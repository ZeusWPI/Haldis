from app import app, db

from admin import admin
from login import login_manager
from models import *
from utils import start_process
from views import *


if __name__ == '__main__':
    app.run()
 
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')
