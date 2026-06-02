from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import EmbeddingService


class SearchService:

    @staticmethod
    def search(
        db: Session,
        query: str,
        limit: int = 3
    ):
        embedding = EmbeddingService.generate(query)

        sql = text("""
            SELECT
                title,
                content,
                embedding <=> CAST(:embedding AS vector) as distance
            FROM knowledge_chunks
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = db.execute(
            sql,
            {
                "embedding": str(embedding),
                "limit": limit
            }
        )

        return result.fetchall()