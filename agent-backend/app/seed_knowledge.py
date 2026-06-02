# app/seed_knowledge.py

from app.db.database import SessionLocal
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.services.embedding_service import EmbeddingService

documents = [
    (
        "Stripe Checkout",
        "Stripe Checkout permite criar uma página hospedada para receber pagamentos."
    ),
    (
        "Stripe Webhooks",
        "Webhooks Stripe notificam sua aplicação quando um pagamento é concluído."
    ),
    (
        "Telegram Bot",
        "Bots do Telegram podem enviar mensagens, fotos e botões interativos."
    ),
    (
        "PostgreSQL",
        "PostgreSQL é um banco de dados relacional open source."
    ),
    (
        "pgvector",
        "pgvector adiciona busca vetorial ao PostgreSQL."
    )
]

db = SessionLocal()

for title, content in documents:
    embedding = EmbeddingService.generate(content)

    KnowledgeChunkRepository.create(
        db=db,
        title=title,
        content=content,
        embedding=embedding
    )

print("Seed concluído")