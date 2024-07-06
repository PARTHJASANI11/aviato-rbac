"""added additional fields in the users table

Revision ID: 30db338162c4
Revises: d4ac98e07fed
Create Date: 2024-07-06 20:12:46.834419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30db338162c4'
down_revision: Union[str, None] = 'd4ac98e07fed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('company_name', sa.String(length=50), nullable=True), schema='rbac')
    op.add_column('users', sa.Column('mobile_number', sa.String(length=10), nullable=True), schema='rbac')
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True), schema='rbac')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=True,
               schema='rbac')
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=250),
               nullable=True,
               schema='rbac')


def downgrade() -> None:
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=250),
               nullable=False,
               schema='rbac')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               schema='rbac')
    op.drop_column('users', 'date_of_birth', schema='rbac')
    op.drop_column('users', 'mobile_number', schema='rbac')
    op.drop_column('users', 'company_name', schema='rbac')
