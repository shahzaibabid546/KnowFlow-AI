from pathlib import Path

from langchain_core.documents import Document

from app.loaders.text_loader import TXTLoader
from app.loaders.pdf_loader import PDFLoader

class UniversalDocumentLoader:
    def load(self,file_paths:list[str]) ->list[Document]:
        all_documents=[]

        for file_path in file_paths:
            path=Path(file_path)
            if path.suffix.lower()==".txt":
                loader=TXTLoader()

            elif path.suffix.lower()==".pdf":
                loader=PDFLoader()

            else:
                raise ValueError(f"UnSupported file Format:{file_path}")

            documents=loader.load([file_path])

            all_documents.extend(documents)

        return all_documents