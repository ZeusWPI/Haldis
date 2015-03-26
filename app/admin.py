from flask import url_for, redirect
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login


from app import app, db
from models import User
from utils import send_command


class ModelBaseView(ModelView):

    def is_accessible(self):
        if login.current_user.is_anonymous():
            return False

        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    column_searchable_list = ('username',)
    inline_models = None
    form_columns = ('username', 'admin')

admin = Admin(app, name='FoodBot', url='/foodbot/admin', template_mode='bootstrap3')

admin.add_view(UserAdminModel(User, db.session))
