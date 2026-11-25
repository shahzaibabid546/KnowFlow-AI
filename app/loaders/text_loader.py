from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

class TXTLoader:

    def load(self,file_paths:list[str]) -> list[Document]:

        all_documents=[]
        for file_path in file_paths:
            path=Path(file_path)

            if not path.exists():
                raise ValueError(f"Path is not a file:{file_path}")
            if not path.is_file():
                raise ValueError(f"Path is not a file:{file_path}")
            if path.suffix.lower()!=".txt":
                raise ValueError(f"Not a TXT file:{file_path}")

            loader=TextLoader(file_path=str(path),encoding="utf-8")


            documents=loader.load()

            all_documents.extend(documents)

        return all_documents        
