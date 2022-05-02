"""Create price_modified column

Revision ID: 55013fe95bea
Revises: 9159a6fed021
Create Date: 2022-04-22 01:00:03.729596

"""

# revision identifiers, used by Alembic.
revision = '55013fe95bea'
down_revision = '9159a6fed021'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('order_item', sa.Column('price_modified', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('order_item', 'price_modified')
