"""empty message

Revision ID: 796ae8abfefd
Revises: 8eb2cc6d09d9
Create Date: 2025-04-17 13:43:37.190228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '796ae8abfefd'
down_revision: Union[str, None] = '8eb2cc6d09d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
