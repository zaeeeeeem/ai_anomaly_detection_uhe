"""Add anomaly detection tables

Revision ID: 0b7d26d1a5e1
Revises: 5bb39e5290c0
Create Date: 2026-01-27 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg


# revision identifiers, used by Alembic.
revision: str = "0b7d26d1a5e1"
down_revision: Union[str, None] = "5bb39e5290c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


userrole_enum = pg.ENUM("customer", "admin", name="userrole")
risktype_enum = pg.ENUM("triage", "dosing", "disclaimer", "self_harm", "other", name="risktype")
humanlabel_enum = pg.ENUM("SAFE", "UNSAFE", "BORDERLINE", name="humanlabel")


def upgrade() -> None:
    userrole_enum.create(op.get_bind(), checkfirst=True)
    risktype_enum.create(op.get_bind(), checkfirst=True)
    humanlabel_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column("role", pg.ENUM("customer", "admin", name="userrole", create_type=False), nullable=False, server_default="customer"),
    )

    op.create_table(
        "interaction_logs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_interaction_logs_timestamp"),
        "interaction_logs",
        ["timestamp"],
        unique=False,
    )

    op.create_table(
        "record_analyses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("risk_context_flags", sa.JSON(), nullable=False),
        sa.Column("hallucination_hints", sa.JSON(), nullable=False),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["interaction_logs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "scoring_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("scores", sa.JSON(), nullable=False),
        sa.Column("flags", sa.JSON(), nullable=False),
        sa.Column("is_flagged", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("scored_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["interaction_logs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_scoring_records_is_flagged"),
        "scoring_records",
        ["is_flagged"],
        unique=False,
    )

    op.create_table(
        "explanation_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("risk_type", pg.ENUM("triage", "dosing", "disclaimer", "self_harm", "other", name="risktype", create_type=False), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("citations", sa.JSON(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["interaction_logs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "feedback_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("human_label", pg.ENUM("SAFE", "UNSAFE", "BORDERLINE", name="humanlabel", create_type=False), nullable=False),
        sa.Column("corrected_response", sa.Text(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("reviewer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["interaction_logs.id"]),
        sa.ForeignKeyConstraint(["reviewer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_table("feedback_records")
    op.drop_table("explanation_records")
    op.drop_index(op.f("ix_scoring_records_is_flagged"), table_name="scoring_records")
    op.drop_table("scoring_records")
    op.drop_table("record_analyses")
    op.drop_index(op.f("ix_interaction_logs_timestamp"), table_name="interaction_logs")
    op.drop_table("interaction_logs")

    op.drop_column("users", "role")

    humanlabel_enum.drop(op.get_bind(), checkfirst=True)
    risktype_enum.drop(op.get_bind(), checkfirst=True)
    userrole_enum.drop(op.get_bind(), checkfirst=True)
