
from typing import Any

from app.retrieval.keyword_retriever import KeywordRetriever
from app.storage.document_store import InMemoryDocumentStore


class RetrievalService:

    def __init__(
        self,
        document_store: InMemoryDocumentStore,
        top_k: int = 3
    ):
        self.document_store = document_store
        self.retriever = KeywordRetriever(top_k=top_k)

    def retrieve(self, query: str) -> list[Any]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        documents = self.document_store.get_documents()

        if not documents:
            return []

        results = self.retriever.retrieve(
            query=query,
            documents=documents
        )

        return results
