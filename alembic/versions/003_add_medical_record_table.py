"""Add medical_record table

Revision ID: 003
Revises: 002
Create Date: 2025-12-01 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('medical_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idanimal', sa.Integer(), nullable=False),
    sa.Column('idveterinarian', sa.Integer(), nullable=False),
    sa.Column('visitdate', sa.DateTime(), nullable=True),
    sa.Column('diagnosis', sa.Text(), nullable=True),
    sa.Column('treatment', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['idanimal'], ['animal.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idveterinarian'], ['veterinarian.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_record_id'), 'medical_record', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_medical_record_id'), table_name='medical_record')
    op.drop_table('medical_record')
