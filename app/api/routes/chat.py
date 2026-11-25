
from fastapi import APIRouter, HTTPException, Request

from app.schemas.chat import ChatMessage


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# Create New Chat Session
@router.post("/sessions")
def create_chat_session(request: Request):

    conversation_service = request.app.state.conversation_service

    session = conversation_service.create_conversation()

    return {
        "message": "Chat session created successfully.",
        "session_id": session.session_id
    }


# Send Message to AI
@router.post("/sessions/{session_id}/messages")
def send_chat_message(
    session_id: str,
    content: str,
    request: Request
):

    conversation_service = request.app.state.conversation_service

    try:

        response = conversation_service.send_message(
            session_id=session_id,
            content=content
        )

        return response

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# Get Conversation History
@router.get("/sessions/{session_id}")
def get_chat_history(
    session_id: str,
    request: Request
):

    conversation_service = request.app.state.conversation_service

    try:

        history = conversation_service.get_conversation_history(
            session_id
        )

        return {
            "session_id": session_id,
            "total_messages": len(history),
            "messages": history
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# Delete Chat Session
@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: str,
    request: Request
):

    conversation_service = request.app.state.conversation_service

    deleted = conversation_service.delete_conversation(
        session_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Chat session not found."
        )

    return {
        "message": "Chat session deleted successfully."
    }
