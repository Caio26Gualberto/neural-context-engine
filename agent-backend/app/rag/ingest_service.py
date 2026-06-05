import hashlib
import re
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.repositories.knowledge_document_repository import KnowledgeDocumentRepository
from app.services.embedding_service import EmbeddingService


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_sections(content: str) -> list[tuple[str, str]]:
    """Split markdown by ## headings. Returns list of (heading, body) tuples."""
    sections = []
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        if body:
            sections.append((heading, body))

    return sections


def _ingest_file(db: Session, filepath: Path) -> None:
    filename = filepath.name
    raw = filepath.read_text(encoding="utf-8")
    file_hash = _sha256(raw)

    doc = KnowledgeDocumentRepository.find_by_filename(db, filename)

    if doc and doc.file_hash == file_hash:
        print(f"  [{filename}] sem alterações — ignorado.")
        return

    sections = _parse_sections(raw)
    if not sections:
        print(f"  [{filename}] nenhuma seção ## encontrada — ignorado.")
        return

    first_h1 = re.search(r"^# (.+)$", raw, re.MULTILINE)
    doc_title = first_h1.group(1).strip() if first_h1 else filename

    if not doc:
        doc = KnowledgeDocumentRepository.create(
            db=db,
            filename=filename,
            title=doc_title,
            file_hash=file_hash,
        )
        existing_chunks: dict[str, object] = {}
        print(f"  [{filename}] novo documento criado.")
    else:
        existing = KnowledgeChunkRepository.find_by_document(db, doc.id)
        existing_chunks = {chunk.title: chunk for chunk in existing}
        print(f"  [{filename}] documento existente — verificando diff...")

    current_titles: set[str] = set()

    for index, (heading, body) in enumerate(sections):
        content_hash = _sha256(body)
        current_titles.add(heading)

        if heading in existing_chunks:
            chunk = existing_chunks[heading]
            if chunk.content_hash == content_hash:
                print(f"    '{heading}' — sem alteração, pulando embedding.")
                continue
            embedding_text = f"{heading}\n\n{body}"
            embedding = EmbeddingService.generate(embedding_text)
            KnowledgeChunkRepository.update(
                db=db,
                chunk=chunk,
                content=body,
                content_hash=content_hash,
                embedding=embedding,
            )
            print(f"    '{heading}' — atualizado.")
        else:
            embedding_text = f"{heading}\n\n{body}"
            embedding = EmbeddingService.generate(embedding_text)
            KnowledgeChunkRepository.create(
                db=db,
                document_id=doc.id,
                chunk_index=index,
                title=heading,
                content=body,
                content_hash=content_hash,
                embedding=embedding,
            )
            print(f"    '{heading}' — inserido.")

    stale_titles = set(existing_chunks.keys()) - current_titles
    for title in stale_titles:
        KnowledgeChunkRepository.delete(db=db, chunk=existing_chunks[title])
        print(f"    '{title}' — removido (não existe mais no arquivo).")

    KnowledgeDocumentRepository.update_hash(db=db, doc=doc, file_hash=file_hash)
    print(f"  [{filename}] concluído.")


class IngestService:

    @staticmethod
    def run(knowledge_dir: Path) -> None:
        if not knowledge_dir.exists():
            print(f"Pasta '{knowledge_dir}' não encontrada.")
            return

        files = sorted(knowledge_dir.glob("*.md"))
        if not files:
            print(f"Nenhum arquivo .md encontrado em '{knowledge_dir}'.")
            return

        print(f"Iniciando ingestão de {len(files)} arquivo(s)...\n")
        db = SessionLocal()
        try:
            for filepath in files:
                _ingest_file(db, filepath)
        finally:
            db.close()

        print("\nIngestão concluída.")
