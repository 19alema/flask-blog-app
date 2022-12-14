"""updating models

Revision ID: 2d58391ae201
Revises: 38c436456f29
Create Date: 2022-11-19 17:13:57.069078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d58391ae201'
down_revision = '38c436456f29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authors', sa.Column('username', sa.String(), nullable=True))
    op.drop_column('profiles', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('authors', 'username')
    # ### end Alembic commands ###
