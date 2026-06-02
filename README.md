# AI Agent

A study project exploring AI engineering concepts: **RAG**, **MCP**, **LLM streaming**, **vector search**, and **document ingestion**.

```
AI-agent/
├── agent-backend/   # FastAPI + PostgreSQL + pgvector + OpenAI
└── frontend/        # React chatbot (Nexus) with streaming UI
```

---

## What this project covers

| Concept | Implementation |
|---------|----------------|
| **RAG** | Documents are embedded with OpenAI and stored in pgvector. On each query the top-k most similar chunks are retrieved and injected into the LLM prompt. |
| **Vector search** | pgvector cosine similarity (`<=>`) over `vector(1536)` embeddings |
| **LLM streaming** | OpenAI `stream=True` piped through FastAPI `StreamingResponse` as SSE, consumed token-by-token in the React frontend |
| **Document ingestion** | Scripts to embed and store arbitrary text documents into the knowledge base |
| **MCP** | Placeholder for Model Context Protocol integration (in progress) |

---

## Quick start

### 1. Start the database

```bash
cd agent-backend
docker compose up -d
```

PostgreSQL 18 with pgvector runs on port **5433**.

### 2. Set up the backend

```bash
cd agent-backend
cp .env.example .env        # fill in OPENAI_API_KEY
pip install -r requirements.txt
alembic upgrade head        # run migrations
python -m app.seed_knowledge  # embed and store sample documents
python -m uvicorn app.main:app --reload
```

Backend available at `http://localhost:8000`

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend (Nexus chatbot) available at `http://localhost:5173`

---

## Useful scripts (run from `agent-backend/`)

| Command | Description |
|---------|-------------|
| `python -m app.seed_knowledge` | Embed and insert sample documents into the knowledge base |
| `python -m app.ingest` | Ingest a single custom document |
| `python -m app.test_search` | Run a semantic search query and print results |
| `python -m app.test_connection` | Verify database connectivity |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade base` | Roll back all migrations |

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ask` | Returns a complete answer (waits for full response) |
| `POST` | `/ask/stream` | Streams the answer token by token via SSE |

```json
{ "question": "How does Stripe Checkout work?" }
```

See `agent-backend/README.md` for the full backend setup guide.
