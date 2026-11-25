
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFLoader:

    def load(self, file_paths: list[str]) -> list[Document]:

        all_documents = []

        for file_path in file_paths:

            path = Path(file_path)

            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            if not path.is_file():
                raise ValueError(f"Path is not a file: {file_path}")

            if path.suffix.lower() != ".pdf":
                raise ValueError(f"Not a PDF file: {file_path}")

            loader = PyPDFLoader(str(path))

            documents = loader.load()

            all_documents.extend(documents)

        return all_documents
