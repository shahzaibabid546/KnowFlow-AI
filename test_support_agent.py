
from app.services.document_service import DocumentIngestionService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.llm.gemini_provider import GeminiProvider
from app.services.rag_service import RAGService

from app.agents.support_agent.graph import create_support_agent


# Step 1: Load Company Documents
ingestion_service = DocumentIngestionService()

document_paths = [
    "sample_documents/company_policy.txt",
    "sample_documents/refund_policy.txt"
]

ingestion_service.ingest_documents(document_paths)


# Step 2: Initialize Retrieval Service
retrieval_service = RetrievalService(
    document_store=ingestion_service.document_store
)


# Step 3: Initialize Context Builder
context_builder = ContextBuilder()


# Step 4: Initialize Gemini Provider
gemini_provider = GeminiProvider()


# Step 5: Initialize RAG Service
rag_service = RAGService(
    retrieval_service=retrieval_service,
    context_builder=context_builder,
    gemini_provider=gemini_provider
)


# Step 6: Create LangGraph Support Agent
support_agent = create_support_agent(
    rag_service=rag_service
)


# Step 7: Prepare Initial State
initial_state = {
    "question": "Can I get a refund within 14 days of purchase?",
    "answer": "",
    "sources": [],
    "retry_count": 0,
    "max_retries": 2,
    "answer_status": "pending",
    "needs_human": False,
    "escalation_reason": ""
}


# Step 8: Execute Support Agent
result = support_agent.invoke(initial_state)


# Step 9: Display Final Result
print("\n========== KNOWFLOW AI SUPPORT AGENT ==========")

print("\nCustomer Question:")
print(result["question"])

print("\nGenerated Answer:")
print(result["answer"])

print("\nAnswer Status:")
print(result["answer_status"])

print("\nSources:")
for source in result["sources"]:
    print("-", source)

print("\nRetry Count:")
print(result["retry_count"])

print("\nHuman Support Required:")
print(result["needs_human"])

print("\nEscalation Reason:")
print(result["escalation_reason"])

print("\n========== TEST COMPLETED ==========")
