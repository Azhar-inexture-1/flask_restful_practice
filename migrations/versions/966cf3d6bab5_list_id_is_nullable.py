"""List id is nullable

Revision ID: 966cf3d6bab5
Revises: d9f501e06f3a
Create Date: 2022-08-22 14:48:34.315810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '966cf3d6bab5'
down_revision = 'd9f501e06f3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###