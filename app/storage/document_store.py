
from langchain_core.documents import Document


class InMemoryDocumentStore:

    def __init__(self):

        self.documents: list[Document] = []

    def add_documents(self, documents: list[Document]) -> None:

        self.documents.extend(documents)

    def get_documents(self) -> list[Document]:

        return self.documents

    def clear(self) -> None:

        self.documents.clear()
