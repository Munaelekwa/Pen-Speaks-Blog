"""empty message

Revision ID: 8218e3792e66
Revises: 0768c158aadc
Create Date: 2022-11-04 21:23:10.267468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8218e3792e66'
down_revision = '0768c158aadc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpost', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpost', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###