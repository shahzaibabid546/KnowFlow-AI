
import re

from langchain_core.documents import Document


class KeywordRetriever:

    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def retrieve(
        self,
        query: str,
        documents: list[Document]
    ) -> list[Document]:

        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_words = set(
            re.findall(r"\b\w+\b", query.lower())
        )

        scored_documents = []

        for document in documents:

            document_words = set(
                re.findall(
                    r"\b\w+\b",
                    document.page_content.lower()
                )
            )

            matching_words = query_words.intersection(
                document_words
            )

            score = len(matching_words)

            if score > 0:
                scored_documents.append(
                    (score, document)
                )

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True
        )

        relevant_documents = [
            document
            for score, document in scored_documents[:self.top_k]
        ]

        return relevant_documents
