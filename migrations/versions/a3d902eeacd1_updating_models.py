"""updating models

Revision ID: a3d902eeacd1
Revises: 4e9381b98bbb
Create Date: 2022-11-19 17:25:58.886448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3d902eeacd1'
down_revision = '4e9381b98bbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('last_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'last_name')
    # ### end Alembic commands ###