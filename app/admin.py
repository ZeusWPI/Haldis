import flask_login as login
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from models import Order, OrderItem, OrderItemChoice, User


class ModelBaseView(ModelView):
    # pylint: disable=too-few-public-methods, no-self-use
    def is_accessible(self) -> bool:
        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    # pylint: disable=too-few-public-methods
    column_searchable_list = ("username",)
    column_editable_list = ("username",)
    column_default_sort = "username"
    inline_models = None


class OrderAdminModel(ModelBaseView):
    # pylint: disable=too-few-public-methods
    column_list = ["starttime", "stoptime", "location_name", "location_id", "courier"]
    column_labels = {
        "starttime": "Start time", "stoptime": "Closing time",
        "location_name": "Location name", "location_id": "HLDS location ID",
        "courier": "Courier"}
    form_excluded_columns = ["items", "courier_id"]
    column_default_sort = ("starttime", True)
    can_delete = False


class OrderItemAdminModel(ModelBaseView):
    # pylint: disable=too-few-public-methods
    column_default_sort = ("order_id", True)


def init_admin(app: Flask, database: SQLAlchemy) -> None:
    "Register admin views with Flask app."
    admin = Admin(app, name="Haldis", url="/admin", template_mode="bootstrap3")

    admin.add_view(UserAdminModel(User, database.session))
    admin.add_view(OrderAdminModel(Order, database.session))
    admin.add_view(OrderItemAdminModel(OrderItem, database.session))
