
from typing import Any


class ContextBuilder:

    def build_context(self, documents: list[Any]) -> str:

        if not documents:
            return "No relevant information found."

        context_parts = []

        for index, document in enumerate(documents, start=1):

            source = document.metadata.get(
                "source",
                "Unknown source"
            )

            content = document.page_content

            context_part = (
                f"Source {index}: {source}\n"
                f"Content:\n{content}"
            )

            context_parts.append(context_part)

        context = "\n\n".join(context_parts)

        return context