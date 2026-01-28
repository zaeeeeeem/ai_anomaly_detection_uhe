"""Add cascade delete to interaction_logs.conversation_id

Revision ID: 7a8d1f9b4a2b
Revises: 0b7d26d1a5e1
Create Date: 2026-01-27 19:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a8d1f9b4a2b"
down_revision: Union[str, None] = "0b7d26d1a5e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "interaction_logs_conversation_id_fkey",
        "interaction_logs",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "interaction_logs_conversation_id_fkey",
        "interaction_logs",
        "conversations",
        ["conversation_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "interaction_logs_conversation_id_fkey",
        "interaction_logs",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "interaction_logs_conversation_id_fkey",
        "interaction_logs",
        "conversations",
        ["conversation_id"],
        ["id"],
    )
