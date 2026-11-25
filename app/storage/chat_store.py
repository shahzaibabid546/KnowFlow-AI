
from datetime import datetime, timezone

from app.schemas.chat import ChatMessage, ChatSession


class ChatSessionStore:

    def __init__(self):
        # In-memory dictionary for storing chat sessions
        self.sessions: dict[str, ChatSession] = {}

    # Create a New Chat Session
    def create_session(self) -> ChatSession:

        session = ChatSession()

        self.sessions[session.session_id] = session

        return session

    # Get an Existing Chat Session
    def get_session(self, session_id: str) -> ChatSession | None:

        return self.sessions.get(session_id)

    # Add a Message to a Chat Session
    def add_message(
        self,
        session_id: str,
        message: ChatMessage
    ) -> ChatSession:

        session = self.get_session(session_id)

        if session is None:
            raise ValueError("Chat session not found.")

        session.messages.append(message)

        session.updated_at = datetime.now(timezone.utc)

        return session

    # Get Conversation History
    def get_history(self, session_id: str) -> list[ChatMessage]:

        session = self.get_session(session_id)

        if session is None:
            raise ValueError("Chat session not found.")

        return session.messages

    # Delete a Chat Session
    def delete_session(self, session_id: str) -> bool:

        if session_id not in self.sessions:
            return False

        del self.sessions[session_id]

        return True

    # Get All Chat Sessions
    def get_all_sessions(self) -> list[ChatSession]:

        return list(self.sessions.values())
