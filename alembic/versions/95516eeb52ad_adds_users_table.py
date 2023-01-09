"""adds users table

Revision ID: 95516eeb52ad
Revises: c79368f3df56
Create Date: 2023-01-08 17:30:59.832089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95516eeb52ad'
down_revision = 'c79368f3df56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_table('users')
