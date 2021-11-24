"""create users table

Revision ID: 9be06da9fb18
Revises: 0958717ef5e0
Create Date: 2021-11-23 19:58:35.616102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9be06da9fb18'
down_revision = '0958717ef5e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(100), unique=True),
        sa.Column('password', sa.String(200)),
    )


def downgrade():
    op.drop_table('users')
