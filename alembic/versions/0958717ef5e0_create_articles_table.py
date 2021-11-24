"""create articles table

Revision ID: 0958717ef5e0
Revises: 
Create Date: 2021-11-23 13:31:44.402889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0958717ef5e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500)),
    )


def downgrade():
    op.drop_table('articles')
