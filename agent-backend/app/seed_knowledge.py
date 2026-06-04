from pathlib import Path

from app.rag.ingest_service import IngestService

IngestService.run(Path("knowledge"))