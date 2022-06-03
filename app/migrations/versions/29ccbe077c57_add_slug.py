"""add slug

Revision ID: 29ccbe077c57
Revises: 55013fe95bea
Create Date: 2022-05-20 19:46:11.924218

"""

# revision identifiers, used by Alembic.
revision = '29ccbe077c57'
down_revision = '55013fe95bea'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

def upgrade():
    op.add_column('order', sa.Column(
        'slug',
        sa.String(length=8),
        nullable=False,
        # Default: random alphanumerical string
        server_default=text('SUBSTRING(MD5(RAND()) FROM 1 FOR 7)')
    ))
    op.create_unique_constraint('order_slug_unique', 'order', ['slug'])


def downgrade():
    op.drop_constraint('order_slug_unique', 'order', type_='unique')
    op.drop_column('order', 'slug')
