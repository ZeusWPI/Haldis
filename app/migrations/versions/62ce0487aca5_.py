"""empty message

Revision ID: 62ce0487aca5
Revises: 3f76cdeb986d
Create Date: 2023-04-20 22:12:29.384814

"""

# revision identifiers, used by Alembic.
revision = '62ce0487aca5'
down_revision = '3f76cdeb986d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    op.alter_column(
        'order',
        'slug',
        type_=sa.String(length=32),
        nullable=False,
        # Default: random alphanumerical string
        server_default=text('SUBSTRING(MD5(RAND()) FROM 1 FOR 7)')
    )


def downgrade():
    op.alter_column(
        'order',
        'slug',
        type_=sa.String(length=8),
        nullable=False,
        # Default: random alphanumerical string
        server_default=text('SUBSTRING(MD5(RAND()) FROM 1 FOR 7)')
    )
