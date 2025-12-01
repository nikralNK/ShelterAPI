"""Add veterinarian table

Revision ID: 002
Revises: 001
Create Date: 2025-12-01 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('veterinarian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=255), nullable=False),
    sa.Column('specialization', sa.String(length=100), nullable=True),
    sa.Column('phonenumber', sa.String(length=50), nullable=True),
    sa.Column('licensenumber', sa.String(length=100), nullable=True),
    sa.Column('iduser', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['iduser'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_veterinarian_id'), 'veterinarian', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_veterinarian_id'), table_name='veterinarian')
    op.drop_table('veterinarian')
