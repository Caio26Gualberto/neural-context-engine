from datetime import datetime

from sqlalchemy.orm import Session

from app.models.knowledge_document import KnowledgeDocument


class KnowledgeDocumentRepository:

    @staticmethod
    def find_by_filename(db: Session, filename: str) -> KnowledgeDocument | None:
        return (
            db.query(KnowledgeDocument)
            .filter(KnowledgeDocument.filename == filename)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        filename: str,
        title: str,
        file_hash: str,
    ) -> KnowledgeDocument:
        doc = KnowledgeDocument(
            filename=filename,
            title=title,
            file_hash=file_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def update_hash(db: Session, doc: KnowledgeDocument, file_hash: str) -> None:
        doc.file_hash = file_hash
        doc.updated_at = datetime.utcnow()
        db.commit()
