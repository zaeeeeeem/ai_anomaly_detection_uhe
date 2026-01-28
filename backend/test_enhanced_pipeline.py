"""
Test script for Enhanced Pipeline Orchestrator

This script tests the enhanced detection pipeline with sample interactions.
"""

import asyncio
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.interaction_log import InteractionLog
from app.services.enhanced_pipeline_orchestrator import create_enhanced_orchestrator


async def test_enhanced_pipeline():
    """Test the enhanced pipeline with a sample interaction"""

    db = SessionLocal()

    try:
        print("=" * 80)
        print("Testing Enhanced Pipeline Orchestrator")
        print("=" * 80)

        # Create a test interaction
        test_interaction = InteractionLog(
            prompt="What's the capital of France?",
            response="The capital of France is Paris, which has been the capital since 987 AD.",
            model_name="gemini-1.5-flash",
            user_id=1,  # Assuming user ID 1 exists
            conversation_id=1  # Assuming conversation ID 1 exists
        )

        db.add(test_interaction)
        db.commit()
        db.refresh(test_interaction)

        print(f"\n✓ Created test interaction: {test_interaction.id}")
        print(f"  Question: {test_interaction.prompt}")
        print(f"  Response: {test_interaction.response}")

        # Run enhanced pipeline
        print("\n" + "=" * 80)
        print("Running Enhanced Detection Pipeline...")
        print("=" * 80)

        orchestrator = create_enhanced_orchestrator(db)
        result = await orchestrator.run(test_interaction.id)

        # Display results
        print("\n" + "=" * 80)
        print("Pipeline Results")
        print("=" * 80)

        print(f"\n✓ Pipeline completed successfully!")
        print(f"\n  Interaction ID: {result['interaction_id']}")
        print(f"  Is Anomaly: {result['is_anomaly']}")
        print(f"  Anomaly Category: {result['anomaly_category']}")
        print(f"  Final Score: {result['final_score']:.3f}")

        print(f"\n  Dimension Scores:")
        for dimension, score in result['detection_results'].items():
            if dimension == 'quality':
                print(f"    - Quality: {score['overall_quality_score']:.3f}")
            elif dimension == 'hallucination':
                print(f"    - Hallucination Risk: {score['hallucination_risk_score']:.3f}")
            elif dimension == 'alignment':
                print(f"    - Alignment: {score['overall_alignment_score']:.3f}")
            elif dimension == 'safety':
                print(f"    - Safety Risk: {score['safety_risk_score']:.3f}")
            elif dimension == 'confidence':
                print(f"    - Confidence Calibration: {score['calibration_quality']:.3f}")

        # Verify database records were created
        print("\n" + "=" * 80)
        print("Verifying Database Records")
        print("=" * 80)

        db.refresh(test_interaction)

        print(f"\n  ✓ ResponseQuality: {'Created' if test_interaction.quality_analysis else 'Missing'}")
        print(f"  ✓ HallucinationDetection: {'Created' if test_interaction.hallucination_detection else 'Missing'}")
        print(f"  ✓ ContextAlignment: {'Created' if test_interaction.context_alignment else 'Missing'}")
        print(f"  ✓ SafetyAssessment: {'Created' if test_interaction.safety_assessment else 'Missing'}")
        print(f"  ✓ ConfidenceCalibration: {'Created' if test_interaction.confidence_calibration else 'Missing'}")
        print(f"  ✓ AnomalyScore: {'Created' if test_interaction.anomaly_score else 'Missing'}")

        print("\n" + "=" * 80)
        print("Test Completed Successfully! ✓")
        print("=" * 80)

        # Cleanup test data
        print("\nCleaning up test interaction...")
        db.delete(test_interaction)
        db.commit()
        print("✓ Test data cleaned up")

    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    print("\nStarting Enhanced Pipeline Test...\n")
    asyncio.run(test_enhanced_pipeline())
