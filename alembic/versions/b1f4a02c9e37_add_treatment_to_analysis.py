"""add treatment to analysis

Revision ID: b1f4a02c9e37
Revises: a3c7e91b2d04
Create Date: 2026-06-10 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'b1f4a02c9e37'
down_revision: Union[str, None] = 'a3c7e91b2d04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('analysis', sa.Column('treatment', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('analysis', 'treatment')
