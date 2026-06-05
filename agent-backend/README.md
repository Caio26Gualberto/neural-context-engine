# AI Agent — Backend (Banco Nexus)

FastAPI backend powering an internal AI agent for the fictional bank **Banco Nexus**. Implements an agentic RAG pipeline with tool calling, pgvector semantic search, smart document ingestion, and streaming responses.

## Stack

- **FastAPI** — REST API with SSE streaming support
- **PostgreSQL + pgvector** — vector store for `vector(1536)` embeddings
- **SQLAlchemy + Alembic** — ORM and migrations
- **OpenAI** — embeddings (`text-embedding-3-small`), chat + tool calling (`gpt-4.1-mini`)

---

## Architecture

```
POST /ask  or  /ask/stream
      │
      ▼
AgentService.gather_context(question)
  └─ LLM decides which tools to call
  └─ Executes tools in parallel: search_knowledge / get_payment / get_user_balance
  └─ Returns raw context string
      │
      ▼
ChatService.answer(question, context)   ← or stream_answer for SSE
  └─ Final LLM call with natural-tone system prompt + context
  └─ Returns polished response (complete or streamed)
```

### Tools

| Tool | Description |
|------|-------------|
| `search_knowledge` | Semantic search over `knowledge_chunks` via pgvector |
| `get_payment` | Fetch a payment record by ID |
| `get_user_balance` | Fetch a user's current balance |

---

## Project structure

```
app/
├── api/
│   └── chat.py              # POST /ask and /ask/stream endpoints
├── models/
│   ├── knowledge_document.py
│   ├── knowledge_chunk.py
│   ├── user.py
│   └── payment.py
├── repositories/
│   ├── knowledge_document_repository.py
│   ├── knowledge_chunk_repository.py
│   ├── user_repository.py
│   └── payment_repository.py
├── rag/
│   ├── ingest_service.py    # Smart ingestion with SHA-256 diffing
│   └── search_service.py    # pgvector cosine similarity search
├── services/
│   ├── agent_service.py     # Tool calling orchestration
│   ├── chat_service.py      # Final LLM response (complete + streaming)
│   └── embedding_service.py
├── tools/
│   ├── search_knowledge.py
│   ├── get_payment.py
│   ├── get_user_balance.py
│   ├── registry.py
│   └── schemas.py
├── seed_db.py               # 30 users + 150 payments
└── seed_knowledge.py        # Smart-ingest knowledge/*.md

knowledge/
├── pagamentos.md
├── pix.md
├── reembolso.md
├── chargeback.md
├── telegram.md
├── usuarios.md
├── cartao.md
├── fraude.md
└── limites.md
```

---

## 1. Environment

```bash
cp .env.example .env
```

Fill in `.env`:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=ai_agent
DB_USER=postgres
DB_PASSWORD=postgres

OPENAI_API_KEY=sk-...
```

---

## 2. Start the database

```bash
docker compose up -d
```

Spins up PostgreSQL 18 with `pgvector` pre-installed, exposed on port **5433**.

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run migrations

```bash
alembic upgrade head
```

Migrations applied in order:
1. Enable `pgvector` extension
2. Create `knowledge_chunks` (original schema)
3. Create `users` and `payments` tables
4. Create `knowledge_documents`, recreate `knowledge_chunks` with `document_id`, `chunk_index`, `content_hash`

---

## 5. Seed operational data

Inserts 30 users and 150 payments with realistic Brazilian names, varied balances, providers (`pix`, `cartao_credito`, `cartao_debito`, `boleto`, `ted`) and statuses (`pago`, `pendente`, `falhou`, `reembolsado`, `chargeback`). Idempotent.

```bash
python -m app.seed_db
```

---

## 6. Ingest the knowledge base

Reads all `knowledge/*.md` files and embeds each `##` section as a chunk. Re-running is safe — only changed sections are re-embedded, new ones are inserted, and removed ones are deleted.

```bash
python -m app.seed_knowledge
# or equivalently:
python -m app.ingest
```

Embedding text sent to OpenAI includes both the heading and body for better retrieval quality:
```
{heading}\n\n{body}
```

---

## 7. Run the API

```bash
python -m uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ask` | Returns a complete answer |
| `POST` | `/ask/stream` | Streams the answer token by token (SSE) |

#### Request body

```json
{ "question": "Quais são os limites de PIX para conta Premium?" }
```

#### Streaming response format (SSE)

```
data: {"token": "Os"}
data: {"token": " limites"}
...
data: [DONE]
```

---

## 8. Utility scripts

```bash
python -m app.test_search      # semantic search smoke test
python -m app.test_connection  # database connectivity check
alembic upgrade head           # apply pending migrations
alembic downgrade base         # roll back all migrations
```
