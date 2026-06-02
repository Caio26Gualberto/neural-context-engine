from sqlalchemy.orm import Session

from app.models.knowledge_chunk import KnowledgeChunk


class KnowledgeChunkRepository:

    @staticmethod
    def create(
        db: Session,
        title: str,
        content: str,
        embedding: list[float]
    ):
        chunk = KnowledgeChunk(
            title=title,
            content=content,
            embedding=embedding
        )

        db.add(chunk)
        db.commit()

        return chunk