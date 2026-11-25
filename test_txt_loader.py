
from app.loaders.text_loader import TXTLoader


loader = TXTLoader()

file_paths = [
    "sample_documents/company_policy.txt",
    "sample_documents/refund_policy.txt"
]

documents = loader.load(file_paths)

print("Total Documents:", len(documents))

for index, document in enumerate(documents, start=1):

    print(f"\nDocument {index}")
    print("Source:", document.metadata["source"])
    print("Content:")
    print(document.page_content)

    print("-" * 50)
