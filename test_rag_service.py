
from app.services.document_service import DocumentIngestionService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.llm.gemini_provider import GeminiProvider
from app.services.rag_service import RAGService


# Step 1: Load company documents
ingestion_service = DocumentIngestionService()

document_paths = [
    "sample_documents/company_policy.txt",
    "sample_documents/refund_policy.txt"
]

ingestion_service.ingest_documents(document_paths)


# Step 2: Create Retrieval Service
retrieval_service = RetrievalService(
    document_store=ingestion_service.document_store
)


# Step 3: Create Context Builder
context_builder = ContextBuilder()


# Step 4: Create Gemini Provider
gemini_provider = GeminiProvider()


# Step 5: Create RAG Service
rag_service = RAGService(
    retrieval_service=retrieval_service,
    context_builder=context_builder,
    gemini_provider=gemini_provider
)


# Step 6: Ask a question
question = "Can I get a refund within 14 days of purchase?"

result = rag_service.generate_answer(question)


# Step 7: Display the result
print("\nUser Question:")
print(question)

print("\nGenerated Answer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print("-", source)
