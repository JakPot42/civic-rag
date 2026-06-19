from sqlalchemy import Column, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    municipality = Column(String, nullable=False, default="Tiverton")
    state = Column(String, nullable=False, default="RI")
    governing_body = Column(String, nullable=False)
    meeting_date = Column(String, nullable=False)  # ISO date string YYYY-MM-DD
    doc_type = Column(String, nullable=False)       # "minutes" or "agenda"
    source_url = Column(String, nullable=True)


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, nullable=False)
    heading = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    # Denormalized for fast retrieval without join
    municipality = Column(String, nullable=False)
    governing_body = Column(String, nullable=False)
    meeting_date = Column(String, nullable=False)
    doc_title = Column(String, nullable=False)
    source_url = Column(String, nullable=True)

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.id,
            "document_id": self.document_id,
            "heading": self.heading or "",
            "body": self.body,
            "municipality": self.municipality,
            "governing_body": self.governing_body,
            "meeting_date": self.meeting_date,
            "doc_title": self.doc_title,
            "source_url": self.source_url or "",
        }


engine = create_engine(f"sqlite:///{DATABASE_URL}", echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
