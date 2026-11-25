# Document business logic will be implemented here.
from langchain_core.documents import Document

from app.loaders.universal_loader import UniversalDocumentLoader
from app.splitters.document_splitter import DocumentSplitter
from app.storage.document_store import InMemoryDocumentStore

class DocumentIngestionService:

    def __init__(self):

        self.loader=UniversalDocumentLoader()

        self.splitter=DocumentSplitter()

        self.document_store=InMemoryDocumentStore()


    def ingest_documents(self,file_paths:list[str])->list[Document]:
        documents = self.loader.load(file_paths)

        chunks = self.splitter.split(documents)

        self.document_store.add_documents(chunks)

        return chunks
    