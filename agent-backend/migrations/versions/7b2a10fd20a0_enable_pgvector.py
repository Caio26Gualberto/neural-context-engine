"""enable_pgvector

Revision ID: 7b2a10fd20a0
Revises: 
Create Date: 2026-06-02 00:55:57.608308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b2a10fd20a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )


def downgrade():
    op.execute(
        "DROP EXTENSION IF EXISTS vector"
    )
