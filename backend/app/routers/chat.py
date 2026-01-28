import asyncio
import logging
import anyio
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models.user import User
from app.models.conversation import Conversation, ModelType
from app.models.message import Message, MessageRole
from app.schemas.message import MessageCreate, MessageResponse
from app.services.gemini_service import gemini_service
from app.services.ollama_service import ollama_service
from app.services.interaction_service import interaction_service
from app.services.pipeline_orchestrator import pipeline_orchestrator
from app.services.enhanced_pipeline_orchestrator import create_enhanced_orchestrator
from app.utils.dependencies import get_current_active_user

logger = logging.getLogger("pipeline")

router = APIRouter(prefix="/api/chat", tags=["Chat"])


async def run_enhanced_pipeline_background(interaction_id: str):
    """Run enhanced detection pipeline in background with new DB session"""
    from app.database import SessionLocal

    db_task = SessionLocal()
    try:
        orchestrator = create_enhanced_orchestrator(db_task)
        result = await orchestrator.run(interaction_id)
        logger.info(
            "Enhanced pipeline completed interaction_id=%s is_anomaly=%s",
            interaction_id,
            result["is_anomaly"]
        )
    except Exception as e:
        logger.error(
            "Enhanced pipeline failed interaction_id=%s error=%s",
            interaction_id,
            str(e)
        )
    finally:
        db_task.close()


@router.post("/{conversation_id}/message", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Send a message and get AI response

    - **conversation_id**: ID of the conversation
    - **content**: Message content

    Returns the AI's response message
    """
    # Verify conversation ownership
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=message_data.content,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get conversation history for context
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    conversation_history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in messages[:-1]
    ]

    # Generate AI response based on model type
    try:
        if conversation.model_type == ModelType.GEMINI:
            ai_response = await gemini_service.generate_response(
                message=message_data.content,
                model_name=conversation.model_name,
                conversation_history=conversation_history,
            )
        elif conversation.model_type == ModelType.OLLAMA:
            ai_response = await ollama_service.generate_response(
                message=message_data.content,
                model_name=conversation.model_name,
                conversation_history=conversation_history,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid model type",
            )

        # Save AI response
        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response,
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)

        interaction = interaction_service.log_interaction(
            db,
            prompt=message_data.content,
            response=ai_response,
            model_name=conversation.model_name,
            user_id=current_user.id,
            conversation_id=conversation_id,
            metadata_json={
                "model_type": conversation.model_type.value,
                "user_message_id": user_message.id,
                "assistant_message_id": assistant_message.id,
            },
        )

        if settings.ENABLE_AUTO_ANALYSIS:
            logger.info("Scheduling enhanced pipeline interaction_id=%s", interaction.id)

            # Add background task using FastAPI's BackgroundTasks
            background_tasks.add_task(
                run_enhanced_pipeline_background,
                interaction.id
            )
        else:
            logger.info("Auto analysis disabled; skipping pipeline")

        return assistant_message

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}",
        )


@router.get("/models/gemini")
def get_gemini_models():
    """Get available Gemini models"""
    return {"models": gemini_service.get_available_models()}


@router.get("/models/ollama")
async def get_ollama_models():
    """Get available Ollama models"""
    models = await ollama_service.get_available_models()
    return {"models": models}


@router.get("/ollama/status")
async def check_ollama_status():
    """Check if Ollama is running"""
    is_running = await ollama_service.check_connection()
    return {
        "status": "online" if is_running else "offline",
        "url": ollama_service.base_url,
    }
