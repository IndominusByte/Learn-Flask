"""add users

Revision ID: 3353b2a008eb
Revises: 238a398e43dc
Create Date: 2020-03-10 00:22:13.379652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3353b2a008eb'
down_revision = '238a398e43dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###