# KnowFlow AI Frontend

React + TypeScript + Vite frontend for the existing KnowFlow AI FastAPI backend.

## Features

- Overview dashboard and backend health indicator
- AI chat: creates chat sessions, sends messages, displays answers and source documents
- Knowledge Base: uploads PDF/TXT files to `POST /documents/upload`
- Support Tickets: list, create, update status, and delete tickets
- Settings page with API URL and backend health status
- Responsive layout for desktop, tablet, and mobile

## Requirements

- Node.js 20.19+ or 22.12+
- KnowFlow FastAPI backend running at `http://127.0.0.1:8000`

## Run on Windows PowerShell

Open PowerShell in the `frontend` folder:

```powershell
npm install
Copy-Item .env.example .env
npm run dev
```

Open the URL printed by Vite, normally `http://127.0.0.1:5173`.

Build check:

```powershell
npm run build
```

## Backend connection

The frontend reads `VITE_API_BASE_URL` from `.env`.

Default:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The FastAPI backend must allow the frontend origin through CORS. Add this to the backend's FastAPI setup if it is not already configured:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Place the middleware registration after creating `app = FastAPI(...)` and before the app starts serving requests.

## API contract assumptions

This frontend matches the current backend structure shared during development:

- `GET /health`
- `POST /chat/sessions`
- `POST /chat/sessions/{session_id}/messages?content=...` (message is currently a query parameter)
- `GET /chat/sessions/{session_id}`
- `DELETE /chat/sessions/{session_id}`
- `GET /tickets/`
- `POST /tickets/`
- `PATCH /tickets/{ticket_id}`
- `DELETE /tickets/{ticket_id}`
- `POST /documents/upload` (multipart field: `file`)

The current backend does not expose a document-list endpoint or a chat-session-list endpoint, so those are not fabricated in this UI. Ticket creation requires `customer_id` and `session_id`, consistent with the existing `TicketCreate` schema.

## Important

- Keep Gemini API keys in the backend `.env` only. Never put secrets in `VITE_*` variables.
- Current backend uses in-memory chat/ticket/document indexing, so data may reset when the server restarts.
