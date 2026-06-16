"""add image_url to analysis

Revision ID: c2d8f91a3e05
Revises: b1f4a02c9e37
Create Date: 2026-06-11 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'c2d8f91a3e05'
down_revision: Union[str, None] = 'b1f4a02c9e37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('analysis', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('analysis', 'image_url')
