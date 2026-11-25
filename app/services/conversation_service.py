
from typing import Any

from app.storage.chat_store import ChatSessionStore
from app.schemas.chat import ChatMessage


class ConversationService:

    def __init__(
        self,
        chat_store: ChatSessionStore,
        support_agent
    ):
        self.chat_store = chat_store
        self.support_agent = support_agent

    # Create a New Conversation
    def create_conversation(self):

        session = self.chat_store.create_session()

        return session

    # Send Message and Get AI Response
    def send_message(
        self,
        session_id: str,
        content: str
    ) -> dict[str, Any]:

        if not content or not content.strip():
            raise ValueError("Message cannot be empty.")

        # Step 1: Check Chat Session
        session = self.chat_store.get_session(session_id)

        if session is None:
            raise ValueError("Chat session not found.")

        # Step 2: Create User Message
        user_message = ChatMessage(
            role="user",
            content=content
        )

        # Step 3: Save User Message
        self.chat_store.add_message(
            session_id=session_id,
            message=user_message
        )

        # Step 4: Prepare Support Agent State
        initial_state = {
            "question": content,
            "answer": "",
            "sources": [],
            "retry_count": 0,
            "max_retries": 2,
            "answer_status": "pending",
            "needs_human": False,
            "escalation_reason": ""
        }

        # Step 5: Execute Support Agent
        result = self.support_agent.invoke(initial_state)

        # Step 6: Create Assistant Message
        assistant_message = ChatMessage(
            role="assistant",
            content=result.get("answer", ""),
            sources=result.get("sources", [])
        )

        # Step 7: Save Assistant Message
        self.chat_store.add_message(
            session_id=session_id,
            message=assistant_message
        )

        # Step 8: Return Conversation Response
        return {
            "session_id": session_id,
            "answer": assistant_message.content,
            "sources": assistant_message.sources,
            "answer_status": result.get("answer_status"),
            "retry_count": result.get("retry_count", 0),
            "needs_human": result.get("needs_human", False),
            "escalation_reason": result.get("escalation_reason", "")
        }

    # Get Conversation History
    def get_conversation_history(
        self,
        session_id: str
    ) -> list[ChatMessage]:

        return self.chat_store.get_history(session_id)

    # Get Conversation Details
    def get_conversation(self, session_id: str):

        return self.chat_store.get_session(session_id)

    # Delete Conversation
    def delete_conversation(self, session_id: str) -> bool:

        return self.chat_store.delete_session(session_id)
