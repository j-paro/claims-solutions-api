"""Modifying Blacklist Table

Revision ID: f6583740d301
Revises: 1fcfec53bce2
Create Date: 2021-10-26 09:09:39.272737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6583740d301'
down_revision = '1fcfec53bce2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blacklisted_tokens', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_blacklisted_tokens_jti'), ['jti'])
        batch_op.drop_column('blacklisted_on')
        batch_op.drop_column('token')
        batch_op.drop_column('expires_at')

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_companies_name'), ['name'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_companies_name'), type_='unique')

    with op.batch_alter_table('blacklisted_tokens', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expires_at', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('token', sa.VARCHAR(length=500), nullable=False))
        batch_op.add_column(sa.Column('blacklisted_on', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint(batch_op.f('uq_blacklisted_tokens_jti'), type_='unique')

    # ### end Alembic commands ###
