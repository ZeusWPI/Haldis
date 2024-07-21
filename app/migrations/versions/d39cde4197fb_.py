"""empty message

Revision ID: d39cde4197fb
Revises: 89b2c980b663
Create Date: 2024-07-21 03:31:33.205314

"""

# revision identifiers, used by Alembic.
revision = 'd39cde4197fb'
down_revision = '89b2c980b663'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('osm_node_id', sa.String(length=32), nullable=False),
    sa.Column('hlds_id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('opening_hours', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('street', sa.String(length=128), nullable=True),
    sa.Column('housenumber', sa.String(length=32), nullable=True),
    sa.Column('website', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('location_data')
    # ### end Alembic commands ###
