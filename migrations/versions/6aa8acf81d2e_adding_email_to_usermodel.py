"""Adding email to UserModel

Revision ID: 6aa8acf81d2e
Revises: f6583740d301
Create Date: 2021-10-26 17:07:30.567565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa8acf81d2e'
down_revision = 'f6583740d301'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=80)))
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
