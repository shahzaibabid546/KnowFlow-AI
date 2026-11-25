
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.document_service import DocumentIngestionService
from app.services.retrieval_service import RetrievalService
from app.services.context_builder import ContextBuilder
from app.services.rag_service import RAGService

from app.llm.gemini_provider import GeminiProvider

from app.agents.support_agent.graph import create_support_agent

from app.storage.chat_store import ChatSessionStore
from app.services.conversation_service import ConversationService

from app.storage.ticket_store import TicketStore
from app.services.ticket_service import TicketService


# Initialize FastAPI Application
app = FastAPI(
    title="KnowFlow AI",
    description="AI Knowledge and Customer Support Platform",
    version="1.0.0"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Document Service
document_service = DocumentIngestionService()

# Initialize Retrieval Service
retrieval_service = RetrievalService(
    document_store=document_service.document_store
)

# Initialize Context Builder
context_builder = ContextBuilder()

# Initialize Gemini Provider
gemini_provider = GeminiProvider()

# Initialize RAG Service
rag_service = RAGService(
    retrieval_service=retrieval_service,
    context_builder=context_builder,
    gemini_provider=gemini_provider
)

# Initialize LangGraph Support Agent
support_agent = create_support_agent(rag_service)

# Initialize Chat Store
chat_store = ChatSessionStore()

# Initialize Conversation Service
conversation_service = ConversationService(
    chat_store=chat_store,
    support_agent=support_agent
)

# Initialize Ticket Store
ticket_store = TicketStore()

# Initialize Ticket Service
ticket_service = TicketService(
    ticket_store=ticket_store
)

# Register Services in FastAPI Application State
app.state.conversation_service = conversation_service
app.state.ticket_service = ticket_service
app.state.document_service = document_service


# Import and Register Routers
from app.api.routes.chat import router as chat_router
from app.api.routes.tickets import router as ticket_router
from app.api.routes.documents import router as documents_router

app.include_router(chat_router)
app.include_router(ticket_router)
app.include_router(documents_router)


# Health Check Endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "KnowFlow AI"
    }


# Root Endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to KnowFlow AI",
        "docs": "/docs"
    }
