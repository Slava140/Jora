"""fixed tipo

Revision ID: dc60fce11cdf
Revises: 007f7d87b3f9
Create Date: 2024-12-17 16:27:17.837196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc60fce11cdf'
down_revision: Union[str, None] = '007f7d87b3f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('task_id', sa.Integer(), nullable=False))
    op.drop_constraint('comments_project_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'tasks', ['task_id'], ['id'])
    op.drop_column('comments', 'project_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('project_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_project_id_fkey', 'comments', 'tasks', ['project_id'], ['id'])
    op.drop_column('comments', 'task_id')
    # ### end Alembic commands ###