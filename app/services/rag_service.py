
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.llm.gemini_provider import GeminiProvider


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        gemini_provider: GeminiProvider
    ):
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.gemini_provider = gemini_provider

    def generate_answer(self, question: str) -> dict:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        # Step 1: Retrieve relevant documents
        documents = self.retrieval_service.retrieve(question)

        # Step 2: Handle case when no documents are found
        if not documents:
            return {
                "answer": "I could not find relevant information in the available documents.",
                "sources": []
            }

        # Step 3: Build context from retrieved documents
        context = self.context_builder.build_context(documents)

        # Step 4: Create prompt for Gemini
        prompt = f"""
You are a helpful company customer support assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
clearly say that you do not have enough information.

Do not make up facts or information.

Context:
{context}

User Question:
{question}

Provide a clear and helpful answer.
"""

        # Step 5: Generate answer using Gemini
        answer = self.gemini_provider.generate(prompt)

        # Step 6: Collect document sources
        sources = list(dict.fromkeys(
            document.metadata.get("source", "Unknown source")
            for document in documents
        ))

        # Step 7: Return answer and sources
        return {
            "answer": answer,
            "sources": sources
        }
