"""setup treatments table

Revision ID: f1a2b3c4d5e6
Revises: e7f8a91bc2d3
Create Date: 2026-06-14 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'e7f8a91bc2d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS tratamentos")
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
