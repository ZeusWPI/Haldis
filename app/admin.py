"Module for everything related to Admin users"
import flask_login as login
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from models import Order, OrderItem, OrderItemChoice, User


class ModelBaseView(ModelView):
    "Class for the base view of the model"
    # pylint: disable=too-few-public-methods, no-self-use
    def is_accessible(self) -> bool:
        "Function to check if the logged in user is an admin"
        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    "Class for the model of a UserAdmin"
    # pylint: disable=too-few-public-methods
    column_searchable_list = ("username",)
    column_editable_list = ("username",)
    column_default_sort = "username"
    inline_models = None


class OrderAdminModel(ModelBaseView):
    "Class for the model of a OrderAdmin"
    # pylint: disable=too-few-public-methods
    column_default_sort = ("starttime", True)
    column_list = ["starttime", "stoptime", "location_name", "location_id", "courier", "association"]
    column_labels = {
        "starttime": "Start Time",
        "stoptime": "Closing Time",
        "location_id": "HLDS Location ID",
        "association": "Association",
    }
    form_excluded_columns = ["items", "courier_id"]
    can_delete = False


class OrderItemAdminModel(ModelBaseView):
    "Class for the model of a OrderItemAdmin"
    # pylint: disable=too-few-public-methods
    column_default_sort = ("order_id", True)
    column_list = [
        "order_id",
        "order.location_name",
        "user_name",
        "user",
        "dish_name",
        "dish_id",
        "comment",
        "price",
        "paid",
        "hlds_data_version",
    ]
    column_labels = {
        "order_id": "Order",
        "order.location_name": "Order's Location",
        "user_name": "Anon. User",
        "user_id": "Registered User",
        "hlds_data_version": "HLDS Data Version",
        "dish_id": "HLDS Dish ID",
    }


def init_admin(app: Flask, database: SQLAlchemy) -> None:
    "Register admin views with Flask app."
    admin = Admin(app, name="Haldis", url="/admin", template_mode="bootstrap3")

    admin.add_view(UserAdminModel(User, database.session))
    admin.add_view(OrderAdminModel(Order, database.session))
    admin.add_view(OrderItemAdminModel(OrderItem, database.session))
