import uuid

from sqlalchemy.orm import Session

from app.models.knowledge_chunk import KnowledgeChunk


class KnowledgeChunkRepository:

    @staticmethod
    def find_by_document(db: Session, document_id: uuid.UUID) -> list[KnowledgeChunk]:
        return (
            db.query(KnowledgeChunk)
            .filter(KnowledgeChunk.document_id == document_id)
            .order_by(KnowledgeChunk.chunk_index)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        document_id: uuid.UUID,
        chunk_index: int,
        title: str,
        content: str,
        content_hash: str,
        embedding: list[float],
    ) -> KnowledgeChunk:
        chunk = KnowledgeChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            title=title,
            content=content,
            content_hash=content_hash,
            embedding=embedding,
        )
        db.add(chunk)
        db.commit()
        return chunk

    @staticmethod
    def update(
        db: Session,
        chunk: KnowledgeChunk,
        content: str,
        content_hash: str,
        embedding: list[float],
    ) -> None:
        chunk.content = content
        chunk.content_hash = content_hash
        chunk.embedding = embedding
        db.commit()

    @staticmethod
    def delete(db: Session, chunk: KnowledgeChunk) -> None:
        db.delete(chunk)
        db.commit()