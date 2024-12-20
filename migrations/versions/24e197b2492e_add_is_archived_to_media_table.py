"""add is_archived to media table

Revision ID: 24e197b2492e
Revises: 3a8cdb2e0957
Create Date: 2024-12-19 20:38:56.480825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24e197b2492e'
down_revision: Union[str, None] = '3a8cdb2e0957'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media', sa.Column('is_archived', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media', 'is_archived')
    # ### end Alembic commands ###