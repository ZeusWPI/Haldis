"Haldis admin related views and models"

import flask_login as login
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from models import Order, OrderItem, OrderItemChoice, User


class ModelBaseView(ModelView):
    "Base model for admin related things"
    # pylint: disable=R0201, R0903
    def is_accessible(self) -> bool:
        "Check if the user has admin permission"
        if login.current_user.is_anonymous():
            return False
        return login.current_user.is_admin()


class UserAdminModel(ModelBaseView):
    "Model for user admin"
    # pylint: disable=R0903
    column_searchable_list = ("username",)
    inline_models = None


def init_admin(app: Flask, database: SQLAlchemy) -> None:
    "Initialize the admin related things in the app."
    admin = Admin(app, name="Haldis", url="/admin", template_mode="bootstrap3")

    admin.add_view(UserAdminModel(User, database.session))
    admin.add_view(ModelBaseView(Order, database.session))
    admin.add_view(ModelBaseView(OrderItem, database.session))
    admin.add_view(ModelBaseView(OrderItemChoice, database.session))
