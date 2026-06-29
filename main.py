from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from sqlalchemy import select

from config import DEMO_MODE
from models import Document, Chunk, init_db, SessionLocal, get_db
from seed_data import load_seed_data
from search import build_index, BM25Index
from rag import ask
from config import TOP_K

templates = Jinja2Templates(directory="templates")

_index: BM25Index | None = None


def _get_index() -> BM25Index:
    return _index  # type: ignore[return-value]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _index
    init_db()
    with SessionLocal() as db:
        load_seed_data(db)
        chunks = [c.to_dict() for c in db.execute(select(Chunk)).scalars().all()]
    _index = build_index(chunks)
    yield


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Tiverton Civic Intelligence", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


_MAX_QUERY_CHARS = 500

@app.get("/", response_class=HTMLResponse)
@limiter.limit("20/minute")
async def index(request: Request, q: str = ""):
    answer = None
    sources: list[dict] = []
    error = None

    if len(q) > _MAX_QUERY_CHARS:
        error = f"Query too long ({len(q):,} chars). Maximum is {_MAX_QUERY_CHARS} characters."
        q = ""

    if q.strip():
        idx = _get_index()
        if idx is None:
            error = "Search index not ready."
        else:
            retrieved = idx.search(q, top_k=TOP_K)
            try:
                result = ask(q, retrieved)
                answer = result["answer"]
                sources = result["sources"]
            except Exception as exc:
                error = f"Error generating answer: {exc}"

    with SessionLocal() as db:
        docs = db.execute(select(Document).order_by(Document.meeting_date.desc())).scalars().all()
        doc_list = [
            {
                "id": d.id,
                "title": d.title,
                "governing_body": d.governing_body,
                "meeting_date": d.meeting_date,
                "doc_type": d.doc_type,
                "source_url": d.source_url,
            }
            for d in docs
        ]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "question": q,
            "answer": answer,
            "sources": sources,
            "documents": doc_list,
            "error": error,
            "demo_mode": DEMO_MODE,
        },
    )


@app.get("/document/{doc_id}", response_class=HTMLResponse)
async def document_detail(request: Request, doc_id: int):
    with SessionLocal() as db:
        doc = db.get(Document, doc_id)
        if doc is None:
            return HTMLResponse("<h1>Document not found</h1>", status_code=404)
        chunks = (
            db.execute(
                select(Chunk).where(Chunk.document_id == doc_id)
            )
            .scalars()
            .all()
        )

    return templates.TemplateResponse(
        request,
        "document.html",
        {
            "doc": {
                "id": doc.id,
                "title": doc.title,
                "municipality": doc.municipality,
                "state": doc.state,
                "governing_body": doc.governing_body,
                "meeting_date": doc.meeting_date,
                "doc_type": doc.doc_type,
                "source_url": doc.source_url,
            },
            "chunks": [c.to_dict() for c in chunks],
        },
    )


@app.get("/api/stats")
async def stats():
    with SessionLocal() as db:
        doc_count = len(db.execute(select(Document)).scalars().all())
        chunk_count = len(db.execute(select(Chunk)).scalars().all())
        bodies = db.execute(select(Chunk.governing_body)).scalars().all()
        body_set = sorted(set(bodies))
    return {
        "documents": doc_count,
        "chunks": chunk_count,
        "governing_bodies": body_set,
        "municipality": "Tiverton, RI",
        "demo_mode": DEMO_MODE,
    }
