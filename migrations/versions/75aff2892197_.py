"""empty message

Revision ID: 75aff2892197
Revises: 
Create Date: 2018-12-10 20:47:13.061586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75aff2892197'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('all_project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('info_id', sa.Integer(), nullable=True),
    sa.Column('c_name_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('c_name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('project', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('sale_name', sa.String(), nullable=True),
    sa.Column('price_banci', sa.String(), nullable=True),
    sa.Column('date_time', sa.String(), nullable=True),
    sa.Column('readed', sa.Boolean(), nullable=True),
    sa.Column('pink', sa.String(), nullable=True),
    sa.Column('sale_time', sa.String(), nullable=True),
    sa.Column('pink_time', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sale_name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('date_time', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('old_active',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cus_id', sa.Integer(), nullable=True),
    sa.Column('old_genre', sa.String(), nullable=True),
    sa.Column('old_banci', sa.String(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('readcomment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cus_id', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('salecustomerinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('c_name_id', sa.String(), nullable=True),
    sa.Column('dongtai', sa.Text(), nullable=True),
    sa.Column('next_phone', sa.Text(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('date_time', sa.Text(), nullable=True),
    sa.Column('pink_date_time', sa.Text(), nullable=True),
    sa.Column('pink', sa.String(), nullable=True),
    sa.Column('sale_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('school', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('flag', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('salecustomerinfo')
    op.drop_table('readcomment')
    op.drop_table('old_active')
    op.drop_table('log')
    op.drop_table('customer')
    op.drop_table('comment')
    op.drop_table('all_project')
    # ### end Alembic commands ###
