
from app.services.document_service import DocumentIngestionService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.services.rag_service import RAGService

from app.llm.gemini_provider import GeminiProvider

from app.agents.support_agent.graph import create_support_agent

from app.storage.chat_store import ChatSessionStore
from app.services.conversation_service import ConversationService


print("\n========== CONVERSATION SERVICE TEST ==========")


# Step 1: Load Company Documents
print("\nStep 1: Loading Documents...")

ingestion_service = DocumentIngestionService()

document_paths = [
    "sample_documents/refund_policy.txt",
    "sample_documents/company_policy.txt"
]

ingestion_service.ingest_documents(document_paths)

print("Documents Loaded Successfully!")


# Step 2: Initialize Retrieval Service
print("\nStep 2: Initializing Retrieval Service...")

retrieval_service = RetrievalService(
    document_store=ingestion_service.document_store
)

print("Retrieval Service Ready!")


# Step 3: Initialize Context Builder
print("\nStep 3: Initializing Context Builder...")

context_builder = ContextBuilder()

print("Context Builder Ready!")


# Step 4: Initialize Gemini Provider
print("\nStep 4: Initializing Gemini Provider...")

gemini_provider = GeminiProvider()

print("Gemini Provider Ready!")


# Step 5: Initialize RAG Service
print("\nStep 5: Initializing RAG Service...")

rag_service = RAGService(
    retrieval_service=retrieval_service,
    context_builder=context_builder,
    gemini_provider=gemini_provider
)

print("RAG Service Ready!")


# Step 6: Initialize LangGraph Support Agent
print("\nStep 6: Initializing Support Agent...")

support_agent = create_support_agent(rag_service)

print("Support Agent Ready!")


# Step 7: Initialize Chat Store
print("\nStep 7: Initializing Chat Store...")

chat_store = ChatSessionStore()

print("Chat Store Ready!")


# Step 8: Initialize Conversation Service
print("\nStep 8: Initializing Conversation Service...")

conversation_service = ConversationService(
    chat_store=chat_store,
    support_agent=support_agent
)

print("Conversation Service Ready!")


# Step 9: Create Conversation
print("\nStep 9: Creating New Conversation...")

session = conversation_service.create_conversation()

session_id = session.session_id

print("Conversation Created Successfully!")
print("Session ID:", session_id)


# Step 10: Send Customer Message
print("\nStep 10: Sending Customer Message...")

customer_question = "Can I get a refund within 14 days of purchase?"

print("Customer Question:", customer_question)

response = conversation_service.send_message(
    session_id=session_id,
    content=customer_question
)


# Step 11: Display AI Response
print("\nStep 11: AI Response")

print("Answer:", response["answer"])

print("Sources:", response["sources"])

print("Answer Status:", response["answer_status"])

print("Retry Count:", response["retry_count"])

print("Human Support Required:", response["needs_human"])


# Step 12: Retrieve Conversation History
print("\nStep 12: Checking Conversation History...")

history = conversation_service.get_conversation_history(
    session_id
)

print("Total Messages:", len(history))

for message in history:

    print("\nRole:", message.role)

    print("Content:", message.content)

    print("Sources:", message.sources)


# Step 13: Retrieve Conversation Details
print("\nStep 13: Retrieving Conversation...")

saved_conversation = conversation_service.get_conversation(
    session_id
)

if saved_conversation is not None:

    print("Conversation Retrieved Successfully!")

    print("Session ID:", saved_conversation.session_id)

    print("Total Messages:", len(saved_conversation.messages))


# Step 14: Delete Conversation
print("\nStep 14: Testing Conversation Deletion...")

deleted = conversation_service.delete_conversation(
    session_id
)

print("Conversation Deleted:", deleted)

print(
    "Conversation After Deletion:",
    conversation_service.get_conversation(session_id)
)


print("\n========== TEST COMPLETED ==========")
