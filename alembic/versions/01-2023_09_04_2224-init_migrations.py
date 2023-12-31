"""init migrations

Revision ID: 01
Revises:
Create Date: 2023-09-04 22:24:57.421683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shoppingpoint',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('customer',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('phone_number', sa.String(length=255), nullable=False),
                    sa.Column('shopping_point_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['shopping_point_id'], ['shoppingpoint.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('worker',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('phone_number', sa.String(length=255), nullable=False),
                    sa.Column('shopping_point_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['shopping_point_id'], ['shoppingpoint.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('order',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('create_date', sa.DateTime(), nullable=True),
                    sa.Column('close_date', sa.DateTime(), nullable=True),
                    sa.Column('status', sa.Enum('started', 'ended', 'in process',
                                                'awaiting', 'canceled', name='status'), nullable=True),
                    sa.Column('shopping_point_id', sa.Integer(), nullable=False),
                    sa.Column('customer_id', sa.Integer(), nullable=False),
                    sa.Column('worker_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
                    sa.ForeignKeyConstraint(['shopping_point_id'], ['shoppingpoint.id'], ),
                    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('visit',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('create_date', sa.DateTime(), nullable=True),
                    sa.Column('order_id', sa.Integer(), nullable=True),
                    sa.Column('shopping_point_id', sa.Integer(), nullable=False),
                    sa.Column('customer_id', sa.Integer(), nullable=False),
                    sa.Column('worker_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
                    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
                    sa.ForeignKeyConstraint(['shopping_point_id'], ['shoppingpoint.id'], ),
                    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('order')
    op.drop_table('worker')
    op.drop_table('customer')
    op.drop_table('shoppingpoint')
    # ### end Alembic commands ###
