# AI Agent — Banco Nexus

A study project simulating an internal AI agent for a fictional Brazilian bank (**Banco Nexus**), exploring: **Agentic RAG**, **tool calling**, **LLM streaming**, **vector search**, and **smart document ingestion**.

```
AI-agent/
├── agent-backend/   # FastAPI + PostgreSQL + pgvector + OpenAI
│   ├── app/         # Application code (agent, tools, RAG, models)
│   └── knowledge/   # Markdown knowledge base (9 files, pt-BR)
└── frontend/        # React chatbot (Nexus) with streaming UI
```

---

## What this project covers

| Concept | Implementation |
|---------|----------------|
| **Agentic RAG** | `AgentService` uses tool calling to decide when to search the knowledge base or query operational data, then `ChatService` produces the final natural language response |
| **Tool calling** | OpenAI function calling with three tools: `search_knowledge`, `get_payment`, `get_user_balance` |
| **Vector search** | pgvector cosine similarity (`<=>`) over `vector(1536)` embeddings from `text-embedding-3-small` |
| **Smart ingestion** | SHA-256 file and chunk hashing — only re-embeds changed sections, inserts new ones, deletes removed ones |
| **LLM streaming** | OpenAI `stream=True` piped through FastAPI `StreamingResponse` as SSE, consumed token-by-token in the React frontend |
| **Knowledge hierarchy** | `KnowledgeDocument` → `KnowledgeChunk` with `document_id`, `chunk_index`, `content_hash` |

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
cp .env.example .env          # fill in OPENAI_API_KEY
pip install -r requirements.txt
alembic upgrade head          # run all migrations
python -m app.seed_db         # seed 30 users + 150 payments
python -m app.seed_knowledge  # embed and store knowledge base
python -m uvicorn app.main:app --reload
```

Backend available at `http://localhost:8000` · Swagger at `/docs`

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend (Nexus chatbot) available at `http://localhost:5173`

---

## Knowledge base (`knowledge/`)

Nine markdown files in Portuguese covering Banco Nexus internal policies. Each `##` section becomes one embedded chunk.

| File | Topics |
|------|--------|
| `pagamentos.md` | Payment methods, statuses, processing times, errors |
| `pix.md` | PIX keys, limits, scheduled PIX, QR Code, errors |
| `reembolso.md` | Refund eligibility, process, SLA |
| `chargeback.md` | Chargeback process, motives, timelines, vs. refund |
| `telegram.md` | Bot commands, alerts, security |
| `usuarios.md` | Account creation, KYC tiers, blocking, closure |
| `cartao.md` | Card types, credit limits, CVV, billing, rewards |
| `fraude.md` | Fraud detection, alerts, common scams |
| `limites.md` | Transaction limits by tier (PIX, TED, card, boleto) |

To re-ingest after editing any `.md` file — only changed sections are re-embedded:

```bash
python -m app.seed_knowledge
```

---

## Useful scripts (run from `agent-backend/`)

| Command | Description |
|---------|-------------|
| `python -m app.seed_db` | Insert 30 users and 150 payments with realistic data |
| `python -m app.seed_knowledge` | Smart-ingest all `knowledge/*.md` files |
| `python -m app.ingest` | Same as `seed_knowledge` (alias) |
| `python -m app.test_search` | Run a semantic search query and print results |
| `python -m app.test_connection` | Verify database connectivity |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade base` | Roll back all migrations |

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ask` | Agent gathers context via tools, returns complete answer |
| `POST` | `/ask/stream` | Agent gathers context, streams answer token by token (SSE) |

```json
{ "question": "Quais são os limites de PIX para conta Premium?" }
```

See `agent-backend/README.md` for the full backend setup guide.
