"""adds remaining columns to posts table

Revision ID: 716fd6b47435
Revises: 95516eeb52ad
Create Date: 2023-01-08 17:41:57.302315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '716fd6b47435'
down_revision = '95516eeb52ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created', sa.TIMESTAMP(
        timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('is_published', sa.Boolean(),
                  server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'user_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'created')
    op.drop_column('posts', 'is_published')
    op.drop_column('posts', 'user_id')
