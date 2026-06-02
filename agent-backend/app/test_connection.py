from sqlalchemy import text

from app.db.database import engine

from app.db.database import DATABASE_URL

print(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT version()"))

    print(result.scalar())