
from app.storage.chat_store import ChatSessionStore
from app.schemas.chat import ChatMessage


def test_create_session():
    chat_store = ChatSessionStore()

    session = chat_store.create_session()

    assert session.session_id is not None
    assert chat_store.get_session(session.session_id) == session


def test_add_and_retrieve_messages():
    chat_store = ChatSessionStore()
    session = chat_store.create_session()

    user_message = ChatMessage(
        role="user",
        content="Can I get a refund within 14 days of purchase?"
    )

    assistant_message = ChatMessage(
        role="assistant",
        content="Yes, you can request a refund within 14 days.",
        sources=["refund_policy.txt"]
    )

    chat_store.add_message(session.session_id, user_message)
    chat_store.add_message(session.session_id, assistant_message)

    history = chat_store.get_history(session.session_id)

    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"
    assert history[1].sources == ["refund_policy.txt"]


def test_delete_session():
    chat_store = ChatSessionStore()
    session = chat_store.create_session()

    deleted = chat_store.delete_session(session.session_id)

    assert deleted is True
    assert chat_store.get_session(session.session_id) is None


def test_delete_nonexistent_session():
    chat_store = ChatSessionStore()

    deleted = chat_store.delete_session("invalid-session-id")

    assert deleted is False


def test_get_all_sessions():
    chat_store = ChatSessionStore()

    chat_store.create_session()
    chat_store.create_session()

    sessions = chat_store.get_all_sessions()

    assert len(sessions) == 2
