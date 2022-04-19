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

import sqlalchemy as sa
from alembic import op
from hlds.definitions import location_definitions
from sqlalchemy.sql import column, table, text

LOCATION_LEGACY_TO_HLDS = {
    2: "blauw_kotje",
    3: "ocean_garden",
    4: "delhaize",
    5: "simpizza",
    6: "shell_tankstation",
    7: "pitta_pinte",
    8: "lan_pizza",
    9: "oriental",
    10: "gouden_sate",
    11: "quick",
    12: "dominos",
    13: "stella_di_mare",
    14: "olifantje",
    15: "pauls_boutique",
    16: "fritoloog",
    17: "andromeda",
    19: "pita_cece",
    20: "pita_uniq",
    21: "basic_italian",
    22: "pizza_hut",
    23: "test",
    25: "primadonna_takeaway",
    26: "primadonna_delivery",
    28: "s5",
    29: "fitchen",
    30: "kebab_anadolu",
}


def upgrade():
    # First the simple actions
    op.create_table(
        "order_item_choice",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("choice_id", sa.String(length=64), nullable=True),
        sa.Column("order_item_id", sa.Integer, nullable=False),
        sa.Column("kind", sa.String(length=1), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("value", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(
            ["order_item_id"],
            ["order_item.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "order_item",
        sa.Column("hlds_data_version", sa.String(length=40), nullable=True),
    )
    op.alter_column(
        "order", "courrier_id", new_column_name="courier_id", type_=sa.Integer
    )
    op.alter_column(
        "order_item",
        "extra",
        new_column_name="comment",
        existing_type=sa.String(254),
        type_=sa.Text,
    )
    op.alter_column(
        "order_item", "name", new_column_name="user_name", type_=sa.String(120)
    )

    # ----------------------------------------------------------------------------------------------
    # Migrate historical product data to order items

    # First create the new columns we will populate
    op.add_column(
        "order_item", sa.Column("dish_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "order_item", sa.Column("dish_name", sa.String(length=120), nullable=True)
    )
    op.add_column("order_item", sa.Column("price", sa.Integer(), nullable=True))
    # Brief, ad-hoc table constructs just for our UPDATE statement, see
    # https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute
    order_item = table(
        "order_item",
        column("product_id", sa.Integer),
        column("dish_id", sa.String),
        column("dish_name", sa.String),
        column("price", sa.Integer),
    )
    # Construct and execute queries
    op.execute(
        text(
            """
        UPDATE order_item
        SET dish_name = (SELECT product.name  FROM product WHERE product.id = order_item.product_id),
            price     = (SELECT product.price FROM product WHERE product.id = order_item.product_id)"""
        )
    )
    # Historical product data migrated, drop obsolete column and table
    op.execute(text("ALTER TABLE order_item DROP FOREIGN KEY order_item_ibfk_3"))
    op.drop_column("order_item", "product_id")
    op.drop_table("product")

    # ----------------------------------------------------------------------------------------------
    # Migrate historical location data to orders

    op.execute(text("ALTER TABLE `order` DROP FOREIGN KEY order_ibfk_2"))
    op.alter_column(
        "order",
        "location_id",
        new_column_name="legacy_location_id",
        type_=sa.Integer,
        nullable=True,
    )
    op.add_column(
        "order", sa.Column("location_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "order", sa.Column("location_name", sa.String(length=128), nullable=True)
    )
    # Brief, ad-hoc table constructs just for our UPDATE statement, see
    # https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute
    order = table(
        "order",
        column("legacy_location_id", sa.Integer),
        column("location_id", sa.String),
        column("location_name", sa.String),
    )
    # Construct and execute queries
    new_location_id = [
        order.update()
        .where(order.c.legacy_location_id == old_id)
        .values(location_id=new_id)
        for old_id, new_id in LOCATION_LEGACY_TO_HLDS.items()
    ]
    location_name_from_location = text(
        """
        UPDATE `order`
        SET location_name = (SELECT location.name FROM location
                             WHERE location.id = `order`.legacy_location_id)"""
    )
    for query in chain(new_location_id, [location_name_from_location]):
        op.execute(query)
    # Historical location data migrated, drop obsolete column and table
    op.drop_column("order", "legacy_location_id")
    op.drop_table("location")


def downgrade():
    raise NotImplementedError("Downgrading to before HLDS is not supported")
