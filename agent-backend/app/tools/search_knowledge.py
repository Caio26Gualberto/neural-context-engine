from app.db.database import SessionLocal
from app.rag.search_service import SearchService


def execute(query: str):
    db = SessionLocal()

    try:
        results = SearchService.search(
            db=db,
            query=query,
            limit=7
        )

        return [
            {
                "title": item.title,
                "content": item.content
            }
            for item in results
        ]

    finally:
        db.close()