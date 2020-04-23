"""change table post

Revision ID: b3a6cd83f1a7
Revises: d62920c594ad
Create Date: 2020-03-11 19:08:46.131475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a6cd83f1a7'
down_revision = 'd62920c594ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_title', table_name='posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_posts_title', 'posts', ['title'], unique=1)
    # ### end Alembic commands ###