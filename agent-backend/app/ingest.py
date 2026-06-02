from app.db.database import SessionLocal
from app.repositories.knowledge_chunk_repository import (
    KnowledgeChunkRepository
)
from app.services.embedding_service import (
    EmbeddingService
)

db = SessionLocal()

content = """
    Stripe Checkout permite
    receber pagamentos através
    de uma página hospedada
    pela própria Stripe.
"""

embedding = EmbeddingService.generate(
    content
)

KnowledgeChunkRepository.create(
    db=db,
    title="Stripe Checkout",
    content=content,
    embedding=embedding
)

print("Documento inserido")