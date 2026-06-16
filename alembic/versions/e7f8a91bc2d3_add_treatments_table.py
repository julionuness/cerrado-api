"""add treatments table

Revision ID: e7f8a91bc2d3
Revises: c2d8f91a3e05
Create Date: 2026-06-14 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'e7f8a91bc2d3'
down_revision: Union[str, None] = 'c2d8f91a3e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'treatments',
        sa.Column('id',         postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('disease',    sa.String(),  nullable=False),
        sa.Column('severity',   sa.String(),  nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('status',     sa.String(),  nullable=False),
        sa.Column('steps',      sa.JSON(),    nullable=False),
    )


def downgrade() -> None:
    op.drop_table('treatments')
