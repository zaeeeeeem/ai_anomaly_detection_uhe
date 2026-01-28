"""Add enhanced detection tables for AI response anomaly detection

Revision ID: 9f4e8c2d3b1a
Revises: 8d3d0c7e1f02
Create Date: 2026-01-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9f4e8c2d3b1a"
down_revision: Union[str, None] = "8d3d0c7e1f02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create response_quality_analysis table
    op.create_table(
        'response_quality_analysis',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=False),
        sa.Column('completeness_score', sa.Float(), nullable=False),
        sa.Column('coherence_score', sa.Float(), nullable=False),
        sa.Column('specificity_score', sa.Float(), nullable=False),
        sa.Column('overall_quality_score', sa.Float(), nullable=False),
        sa.Column('quality_issues', sa.JSON(), nullable=False),
        sa.Column('strengths', sa.JSON(), nullable=False),
        sa.Column('has_quality_issues', sa.Boolean(), nullable=True, default=False),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create hallucination_detection table
    op.create_table(
        'hallucination_detection',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('extracted_claims', sa.JSON(), nullable=False),
        sa.Column('verified_claims', sa.JSON(), nullable=False),
        sa.Column('unverified_claims', sa.JSON(), nullable=False),
        sa.Column('hallucination_risk_score', sa.Float(), nullable=False),
        sa.Column('hallucination_markers', sa.JSON(), nullable=False),
        sa.Column('confidence_issues', sa.JSON(), nullable=False),
        sa.Column('recommended_action', sa.String(), nullable=False),
        sa.Column('analysis_metadata', sa.JSON(), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create context_alignment table
    op.create_table(
        'context_alignment',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('intent_match_score', sa.Float(), nullable=False),
        sa.Column('topic_relevance_score', sa.Float(), nullable=False),
        sa.Column('overall_alignment_score', sa.Float(), nullable=False),
        sa.Column('question_coverage', sa.JSON(), nullable=False),
        sa.Column('alignment_issues', sa.JSON(), nullable=False),
        sa.Column('response_category', sa.String(), nullable=False),
        sa.Column('explanation', sa.String(), nullable=True),
        sa.Column('is_misaligned', sa.Boolean(), nullable=True, default=False),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create safety_assessment table
    op.create_table(
        'safety_assessment',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('safety_risk_score', sa.Float(), nullable=False),
        sa.Column('safety_issues', sa.JSON(), nullable=False),
        sa.Column('appropriate_response_given', sa.Boolean(), nullable=True, default=True),
        sa.Column('risk_category', sa.String(), nullable=False),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create confidence_calibration table
    op.create_table(
        'confidence_calibration',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('appropriate_confidence', sa.Float(), nullable=False),
        sa.Column('calibration_quality', sa.Float(), nullable=False),
        sa.Column('overconfidence_markers', sa.JSON(), nullable=False),
        sa.Column('hedging_words', sa.JSON(), nullable=False),
        sa.Column('issues', sa.JSON(), nullable=False),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create anomaly_scores table
    op.create_table(
        'anomaly_scores',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('quality_anomaly_score', sa.Float(), nullable=False),
        sa.Column('hallucination_anomaly_score', sa.Float(), nullable=False),
        sa.Column('alignment_anomaly_score', sa.Float(), nullable=False),
        sa.Column('safety_anomaly_score', sa.Float(), nullable=False),
        sa.Column('confidence_anomaly_score', sa.Float(), nullable=False),
        sa.Column('final_anomaly_score', sa.Float(), nullable=False),
        sa.Column('is_anomaly', sa.Boolean(), nullable=True, default=False),
        sa.Column('anomaly_category', sa.String(), nullable=True),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['interaction_logs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on is_anomaly for faster queries
    op.create_index('ix_anomaly_scores_is_anomaly', 'anomaly_scores', ['is_anomaly'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_anomaly_scores_is_anomaly', table_name='anomaly_scores')
    op.drop_table('anomaly_scores')
    op.drop_table('confidence_calibration')
    op.drop_table('safety_assessment')
    op.drop_table('context_alignment')
    op.drop_table('hallucination_detection')
    op.drop_table('response_quality_analysis')
