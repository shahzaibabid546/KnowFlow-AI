
from langchain_core.documents import Document

from app.services.context_builder import ContextBuilder


def test_build_context_with_documents():
    documents = [
        Document(
            page_content="Customers can request a refund within 14 days of purchase.",
            metadata={"source": "refund_policy.txt"}
        ),
        Document(
            page_content="Customer support is available 24 hours a day.",
            metadata={"source": "company_policy.txt"}
        )
    ]

    context_builder = ContextBuilder()

    context = context_builder.build_context(documents)

    assert "refund_policy.txt" in context
    assert "company_policy.txt" in context
    assert "Customers can request a refund" in context
    assert "Customer support is available" in context


def test_build_context_with_empty_documents():
    context_builder = ContextBuilder()

    context = context_builder.build_context([])

    assert context == "No relevant information found."


def test_build_context_includes_source_labels():
    documents = [
        Document(
            page_content="Test document content.",
            metadata={"source": "test.txt"}
        )
    ]

    context_builder = ContextBuilder()

    context = context_builder.build_context(documents)

    assert "Source 1: test.txt" in context
    assert "Content:" in context
    assert "Test document content." in context
