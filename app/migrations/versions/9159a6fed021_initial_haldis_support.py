"""Initial HLDS support

Revision ID: 9159a6fed021
Revises: 150252c1cdb1
Create Date: 2020-01-26 16:22:00.935963

"""
# pylint: disable=invalid-name

# revision identifiers, used by Alembic.
revision = "9159a6fed021"
down_revision = "150252c1cdb1"

from itertools import chain
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, text

from hlds.definitions import location_definitions
from data.migration import LOCATION_LEGACY_TO_HLDS, DISH_LEGACY_TO_HLDS


def upgrade():
    # First the simple actions
    op.create_table("order_item_choice",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("choice_id", sa.String(length=64), nullable=True),
        sa.Column("order_item_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=1), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("value", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(["order_item_id"], ["order_item.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.add_column("order_item", sa.Column("hlds_data_version", sa.String(length=40), nullable=True))
    op.alter_column("order_item", "paid", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("order", "courrier_id", new_column_name="courier_id")
    op.alter_column("order_item", "extra", new_column_name="comment",
                    existing_type=sa.String(254), type_=sa.Text())
    op.alter_column("order_item", "name", new_column_name="user_name")

    #----------------------------------------------------------------------------------------------
    # Migrate historical product data to order items

    # First create the new columns we will populate
    op.add_column("order_item", sa.Column("dish_id", sa.String(length=64), nullable=True))
    op.add_column("order_item", sa.Column("dish_name", sa.String(length=120), nullable=True))
    op.add_column("order_item", sa.Column("price", sa.Integer(), nullable=False))
    # Brief, ad-hoc table constructs just for our UPDATE statement, see
    # https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute
    order_item = table("order_item",
        column("product_id", sa.Integer),
        column("dish_id", sa.String),
        column("dish_name", sa.String),
        column("price", sa.Integer)
    )
    # Construct and execute queries
    new_dish_id = [
        order_item.update()
            .where(order_item.c.product_id == old_id)
            .values(dish_id=new_id)
        for old_id, new_id in DISH_LEGACY_TO_HLDS.items()
    ]
    dish_name_and_price_from_product = text("""
        UPDATE order_item
        SET dish_name = (SELECT name  FROM product WHERE product.id == order_item.product_id),
            price     = (SELECT price FROM product WHERE product.id == order_item.product_id)"""
    )
    for query in chain(new_dish_id, [dish_name_and_price_from_product]):
        op.execute(query)
    # Historical product data migrated, drop obsolete column and table
    op.drop_constraint(None, "order_item", type_="foreignkey")
    op.drop_column("order_item", "product_id")
    op.drop_table("product")

    #----------------------------------------------------------------------------------------------
    # Migrate historical location data to orders

    op.add_column("order", sa.Column("location_name", sa.String(length=128), nullable=True))
    op.alter_column("order", "location_id", new_column_name="legacy_location_id")
    # Brief, ad-hoc table constructs just for our UPDATE statement, see
    # https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute
    order = table("order",
        column("legacy_location_id", sa.Integer),
        column("location_id", sa.String),
        column("location_name", sa.String)
    )
    # Construct and execute queries
    new_location_id = [
        order.update()
            .where(order.c.legacy_location_id == old_id)
            .values(location_id=new_id)
        for old_id, new_id in LOCATION_LEGACY_TO_HLDS.items()
    ]
    location_name_from_location = text("""
        UPDATE order
        SET location_name = (SELECT name FROM location
                             WHERE location.id == order.legacy_location_id)"""
    )
    for query in chain(new_location_id, [location_name_from_location]):
        op.execute(query)
    # Historical location data migrated, drop obsolete column and table
    op.drop_column("order", "legacy_location_id")
    op.drop_constraint(None, "order", type_="foreignkey")
    op.drop_table("location")


def downgrade():
    "Don't use this. It will cripple the data."

    op.alter_column("order_item", "paid", existing_type=sa.Boolean(), nullable=True)
    op.alter_column("order", "courier_id", new_column_name="courrier_id")
    op.alter_column("order_item", "comment", new_column_name="extra",
                    existing_type=sa.Text(), type_=sa.String(254))
    op.alter_column("order_item", "user_name", new_column_name="name")

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("order_item", sa.Column("product_id", sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, "order_item", "product", ["product_id"], ["id"])
    op.drop_column("order_item", "price")
    op.drop_column("order_item", "hlds_data_version")
    op.drop_column("order_item", "dish_name")
    op.drop_column("order_item", "dish_id")
    op.create_foreign_key(None, "order", "location", ["location_id"], ["id"])
    op.drop_column("order", "location_name")
    op.create_table("location",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=120), nullable=False),
        sa.Column("address", sa.VARCHAR(length=254), nullable=True),
        sa.Column("website", sa.VARCHAR(length=120), nullable=True),
        sa.Column("telephone", sa.VARCHAR(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table("product",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("location_id", sa.INTEGER(), nullable=True),
        sa.Column("name", sa.VARCHAR(length=120), nullable=False),
        sa.Column("price", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(["location_id"], ["location.id"], ),
        sa.PrimaryKeyConstraint("id")
    )
    op.drop_table("order_item_choice")
    # ### end Alembic commands ###
