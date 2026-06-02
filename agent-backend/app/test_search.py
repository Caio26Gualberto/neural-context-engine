from app.db.database import SessionLocal
from app.rag.search_service import SearchService

db = SessionLocal()

results = SearchService.search(
    db,
    "Como recebo confirmação de pagamento?"
)

for row in results:
    print(row)