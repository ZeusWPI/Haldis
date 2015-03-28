from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login


from app import app, db
from models import User, Location, Product, Order, OrderItem


class ModelBaseView(ModelView):

    def is_accessible(self):
        if login.current_user.is_anonymous():
            return False

        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    column_searchable_list = ('username',)
    inline_models = None


class LocationAdminModel(ModelBaseView):
    column_searchable_list = ('name', 'address', 'website')
    inline_models = None
    form_columns = ('name', 'address', 'website')


admin = Admin(app, name='FoodBot', url='/admin', template_mode='bootstrap3')


admin.add_view(UserAdminModel(User, db.session))
admin.add_view(LocationAdminModel(Location, db.session))
admin.add_view(ModelBaseView(Product, db.session))
admin.add_view(ModelBaseView(Order, db.session))
admin.add_view(ModelBaseView(OrderItem, db.session))
