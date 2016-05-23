"""empty message

Revision ID: 54f638c74711
Revises: fd13360940d6
Create Date: 2016-05-15 17:26:20.351526

"""

# revision identifiers, used by Alembic.
revision = '54f638c74711'
down_revision = 'fd13360940d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'birthday',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('order', 'email',
               existing_type=sa.VARCHAR(length=254),
               nullable=False)
    op.alter_column('order', 'name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('order', 'state',
               existing_type=sa.VARCHAR(length=2),
               nullable=False)
    op.alter_column('order', 'zipcode',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'zipcode',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    op.alter_column('order', 'state',
               existing_type=sa.VARCHAR(length=2),
               nullable=True)
    op.alter_column('order', 'name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('order', 'email',
               existing_type=sa.VARCHAR(length=254),
               nullable=True)
    op.alter_column('order', 'birthday',
               existing_type=sa.DATE(),
               nullable=True)
    ### end Alembic commands ###
