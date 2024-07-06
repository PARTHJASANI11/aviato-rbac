"""updated some fields

Revision ID: ca30347efd9d
Revises: 30db338162c4
Create Date: 2024-07-06 22:55:40.347879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca30347efd9d'
down_revision: Union[str, None] = '30db338162c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('hash_tag', sa.ARRAY(sa.String(length=100)), nullable=True), schema='rbac')
    op.drop_constraint('users_email_key', 'users', schema='rbac', type_='unique')
    op.create_unique_constraint(None, 'users', ['company_name'], schema='rbac')
    op.create_unique_constraint(None, 'users', ['mobile_number'], schema='rbac')


def downgrade() -> None:
    op.drop_constraint(None, 'users', schema='rbac', type_='unique')
    op.drop_constraint(None, 'users', schema='rbac', type_='unique')
    op.create_unique_constraint('users_email_key', 'users', ['email'], schema='rbac')
    op.drop_column('users', 'hash_tag', schema='rbac')