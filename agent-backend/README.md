# AI Agent — Backend

FastAPI backend with RAG (Retrieval-Augmented Generation), pgvector semantic search, OpenAI LLM integration, and Alembic migrations.

## Stack

- **FastAPI** — REST API with streaming support
- **PostgreSQL + pgvector** — vector store for embeddings
- **SQLAlchemy + Alembic** — ORM and migrations
- **OpenAI** — embeddings (`text-embedding-3-small`) and chat (`gpt-4.1-mini`)

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

This spins up a PostgreSQL 18 container with the `pgvector` extension pre-installed, exposed on port **5433**.

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

This applies all migrations in order:
1. Enables the `pgvector` extension
2. Creates the `knowledge_chunks` table with a `vector(1536)` embedding column

---

## 5. Seed the knowledge base

Inserts a set of sample documents, generates embeddings via OpenAI and stores them in the database.

```bash
python -m app.seed_knowledge
```

---

## 6. Ingest a custom document

Ingests a single hardcoded document (Stripe Checkout example). Edit `app/ingest.py` to change the content.

```bash
python -m app.ingest
```

---

## 7. Test semantic search

Runs a similarity search query against the knowledge base and prints the top results.

```bash
python -m app.test_search
```

---

## 8. Test database connection

```bash
python -m app.test_connection
```

---

## 9. Run the API

```bash
python -m uvicorn app.main:app --reload
```

API available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ask` | Returns a complete answer |
| `POST` | `/ask/stream` | Streams the answer token by token (SSE) |

#### Request body (both endpoints)

```json
{ "question": "How does Stripe Checkout work?" }
```
