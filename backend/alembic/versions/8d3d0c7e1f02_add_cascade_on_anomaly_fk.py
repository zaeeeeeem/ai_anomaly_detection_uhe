"""Add cascade delete to anomaly record FKs

Revision ID: 8d3d0c7e1f02
Revises: 7a8d1f9b4a2b
Create Date: 2026-01-27 19:12:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8d3d0c7e1f02"
down_revision: Union[str, None] = "7a8d1f9b4a2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "record_analyses_id_fkey",
        "record_analyses",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "record_analyses_id_fkey",
        "record_analyses",
        "interaction_logs",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "scoring_records_id_fkey",
        "scoring_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "scoring_records_id_fkey",
        "scoring_records",
        "interaction_logs",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "explanation_records_id_fkey",
        "explanation_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "explanation_records_id_fkey",
        "explanation_records",
        "interaction_logs",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "feedback_records_id_fkey",
        "feedback_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "feedback_records_id_fkey",
        "feedback_records",
        "interaction_logs",
        ["id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "feedback_records_id_fkey",
        "feedback_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "feedback_records_id_fkey",
        "feedback_records",
        "interaction_logs",
        ["id"],
        ["id"],
    )

    op.drop_constraint(
        "explanation_records_id_fkey",
        "explanation_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "explanation_records_id_fkey",
        "explanation_records",
        "interaction_logs",
        ["id"],
        ["id"],
    )

    op.drop_constraint(
        "scoring_records_id_fkey",
        "scoring_records",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "scoring_records_id_fkey",
        "scoring_records",
        "interaction_logs",
        ["id"],
        ["id"],
    )

    op.drop_constraint(
        "record_analyses_id_fkey",
        "record_analyses",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "record_analyses_id_fkey",
        "record_analyses",
        "interaction_logs",
        ["id"],
        ["id"],
    )
