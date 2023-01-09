"""setting up posts table

Revision ID: dc2cfb249565
Revises:
Create Date: 2023-01-08 17:18:08.655611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc2cfb249565'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
