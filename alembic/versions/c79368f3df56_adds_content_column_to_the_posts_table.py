"""Adds content column to the posts table

Revision ID: c79368f3df56
Revises: dc2cfb249565
Create Date: 2023-01-08 17:24:13.416413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c79368f3df56'
down_revision = 'dc2cfb249565'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
