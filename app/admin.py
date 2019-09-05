import flask_login as login
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models import Location, Order, OrderItem, Product, User


class ModelBaseView(ModelView):
    def is_accessible(self):
        if login.current_user.is_anonymous():
            return False

        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    column_searchable_list = ("username",)
    inline_models = None


class ProductAdminModel(ModelBaseView):
    column_searchable_list = ("name",)
    inline_models = None


class LocationAdminModel(ModelBaseView):
    column_searchable_list = ("name", "address", "website")
    inline_models = None
    form_columns = ("name", "address", "website", "telephone")


def init_admin(app, db):
    admin = Admin(app, name="Haldis", url="/admin", template_mode="bootstrap3")

    admin.add_view(UserAdminModel(User, db.session))
    admin.add_view(LocationAdminModel(Location, db.session))
    admin.add_view(ProductAdminModel(Product, db.session))
    admin.add_view(ModelBaseView(Order, db.session))
    admin.add_view(ModelBaseView(OrderItem, db.session))
