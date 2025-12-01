"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2025-12-01 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('passwordhash', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('fullname', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('avatar', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('iduser', sa.Integer(), nullable=False),
    sa.Column('createdat', sa.DateTime(), nullable=True),
    sa.Column('expiresat', sa.DateTime(), nullable=False),
    sa.Column('isrevoked', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['iduser'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)

    op.create_table('guardian',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=255), nullable=False),
    sa.Column('phonenumber', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('registrationdate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guardian_id'), 'guardian', ['id'], unique=False)

    op.create_table('enclosure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enclosure_id'), 'enclosure', ['id'], unique=False)

    op.create_table('animal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('breed', sa.String(length=100), nullable=True),
    sa.Column('dateofbirth', sa.Date(), nullable=True),
    sa.Column('idenclosure', sa.Integer(), nullable=True),
    sa.Column('idguardian', sa.Integer(), nullable=True),
    sa.Column('currentstatus', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('size', sa.String(length=50), nullable=True),
    sa.Column('temperament', sa.String(length=100), nullable=True),
    sa.Column('photo', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['idenclosure'], ['enclosure.id'], ),
    sa.ForeignKeyConstraint(['idguardian'], ['guardian.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_animal_id'), 'animal', ['id'], unique=False)

    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idanimal', sa.Integer(), nullable=False),
    sa.Column('idguardian', sa.Integer(), nullable=False),
    sa.Column('applicationdate', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['idanimal'], ['animal.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idguardian'], ['guardian.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_application_id'), 'application', ['id'], unique=False)

    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iduser', sa.Integer(), nullable=False),
    sa.Column('idanimal', sa.Integer(), nullable=False),
    sa.Column('addeddate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['idanimal'], ['animal.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['iduser'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('iduser', 'idanimal', name='_user_animal_uc')
    )
    op.create_index(op.f('ix_favorite_id'), 'favorite', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_favorite_id'), table_name='favorite')
    op.drop_table('favorite')
    op.drop_index(op.f('ix_application_id'), table_name='application')
    op.drop_table('application')
    op.drop_index(op.f('ix_animal_id'), table_name='animal')
    op.drop_table('animal')
    op.drop_index(op.f('ix_enclosure_id'), table_name='enclosure')
    op.drop_table('enclosure')
    op.drop_index(op.f('ix_guardian_id'), table_name='guardian')
    op.drop_table('guardian')
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
