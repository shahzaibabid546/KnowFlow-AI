
from app.services.document_service import DocumentIngestionService
from app.services.retrieval_service import RetrievalService

# Step 1: Documents ingest karna
ingestion_service = DocumentIngestionService()

document_paths = [
    "sample_documents/company_policy.txt",
    "sample_documents/refund_policy.txt"
]

ingestion_service.ingest_documents(document_paths)

# Step 2: Same Document Store RetrievalService ko dena
retrieval_service = RetrievalService(
    document_store=ingestion_service.document_store
)

# Step 3: Query se relevant documents retrieve karna
query = "refund purchase"

results = retrieval_service.retrieve(
    query=query
)

# Step 4: Results display karna
print("User Query:", query)
print("Total Retrieved Documents:", len(results))

for index, document in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Content:", document.page_content)
    print("Source:", document.metadata.get("source"))
