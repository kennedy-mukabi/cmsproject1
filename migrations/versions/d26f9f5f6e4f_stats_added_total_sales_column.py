"""Stats - Added Total_Sales Column

Revision ID: d26f9f5f6e4f
Revises: 
Create Date: 2021-04-05 19:37:26.018820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd26f9f5f6e4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stats', sa.Column('total_sales', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stats', 'total_sales')
    # ### end Alembic commands ###
