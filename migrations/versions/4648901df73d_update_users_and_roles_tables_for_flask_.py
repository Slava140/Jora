"""update users and roles tables for flask_security

Revision ID: 4648901df73d
Revises: 1bc9a9b7f715
Create Date: 2025-02-26 16:59:52.347434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4648901df73d'
down_revision: Union[str, None] = '1bc9a9b7f715'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('description', sa.String(length=255), nullable=False))
    op.alter_column('roles_users', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('roles_users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('roles_users', 'id')
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.add_column('users', sa.Column('create_datetime', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False))
    op.add_column('users', sa.Column('update_datetime', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False))
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'update_datetime')
    op.drop_column('users', 'create_datetime')
    op.drop_column('users', 'active')
    op.drop_column('users', 'password')
    op.add_column('roles_users', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.alter_column('roles_users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('roles_users', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('roles', 'description')
    # ### end Alembic commands ###
