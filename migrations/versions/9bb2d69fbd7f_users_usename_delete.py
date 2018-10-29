"""users.usename delete

Revision ID: 9bb2d69fbd7f
Revises: a942c4e38ab7
Create Date: 2018-10-23 12:03:43.950967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb2d69fbd7f'
down_revision = 'a942c4e38ab7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    # ### end Alembic commands ###
