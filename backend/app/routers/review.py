from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.interaction_log import InteractionLog
from app.models.feedback_record import FeedbackRecord, HumanLabel
from app.schemas.feedback import FeedbackRecordCreate, FeedbackRecordResponse
from app.utils.admin_dependencies import get_current_admin_user

router = APIRouter(prefix="/api/review", tags=["Review"])


@router.get("/{interaction_id}", response_model=FeedbackRecordResponse)
def get_feedback(
    interaction_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    feedback = (
        db.query(FeedbackRecord)
        .filter(FeedbackRecord.id == interaction_id)
        .first()
    )
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )
    return feedback


@router.post("/{interaction_id}", response_model=FeedbackRecordResponse)
def create_or_update_feedback(
    interaction_id: str,
    payload: FeedbackRecordCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    interaction = (
        db.query(InteractionLog)
        .filter(InteractionLog.id == interaction_id)
        .first()
    )
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found",
        )

    label_value = payload.human_label.upper()
    if label_value not in {"SAFE", "UNSAFE", "BORDERLINE"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid human_label",
        )

    feedback = (
        db.query(FeedbackRecord)
        .filter(FeedbackRecord.id == interaction_id)
        .first()
    )

    if feedback:
        feedback.human_label = HumanLabel[label_value]
        feedback.corrected_response = payload.corrected_response
        feedback.comments = payload.comments
        feedback.reviewer_id = payload.reviewer_id or current_admin.id
    else:
        feedback = FeedbackRecord(
            id=interaction_id,
            human_label=HumanLabel[label_value],
            corrected_response=payload.corrected_response,
            comments=payload.comments,
            reviewer_id=payload.reviewer_id or current_admin.id,
        )
        db.add(feedback)

    db.commit()
    db.refresh(feedback)
    return feedback
