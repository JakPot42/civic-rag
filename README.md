# Civic RAG — Local Government Intelligence Engine

BM25 retrieval-augmented generation over Tiverton, RI town meeting documents — ask plain-language questions about local government decisions and get sourced answers that cite the specific governing body and meeting date behind every claim.

Built to demonstrate that RAG + citation discipline solves the hallucination problem for civic information retrieval, and that this architecture works at the local government scale where most civic tech stops.

**Live demo:** https://civic-rag.onrender.com

---

## What It Does

Local government decisions — zoning, budgets, school contracts, infrastructure — are recorded in meeting minutes that are theoretically public but practically inaccessible. Nobody reads them. Search doesn't work because the vocabulary is hyperlocal. AI without citations makes claims you can't verify.

Civic RAG solves the full problem:

1. **Corpus** — 7 pre-seeded Tiverton, RI meeting documents (Town Council, School Committee, Planning Board, 2024)
2. **Chunk** — documents split on `## ` section headers; 19 indexed chunks with governing body and date metadata
3. **Retrieve** — BM25 finds the most relevant sections for your question (no ONNX model, no GPU, no embeddings)
4. **Answer** — Claude reads retrieved context and answers using only that text; every claim must cite `[Governing Body, Date]`
5. **Refuse** — if the answer isn't in the indexed documents, the system says so rather than inventing it

---

## What's Covered (Tiverton, RI 2024)

| Topic | Source |
|-------|--------|
| Budget / tax rate | Town Council, March 2024 |
| Stafford Road multi-family development — denied | Planning Board, April 2024 |
| Highland Road rezoning | Planning Board, February 2024 |
| Crandall Road open space acquisition (55 acres) | Town Council, May 2024 |
| School budget + STEM curriculum expansion | School Committee, April 2024 |
| Teacher contract negotiation | School Committee, March 2024 |
| High school roof replacement | School Committee, February 2024 |
| Road paving schedule | Town Council, April 2024 |
| Water / sewer rate increase | Town Council, March 2024 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Python |
| Retrieval | Pure-Python BM25 (k1=1.5, b=0.75) — no ONNX, no Torch, no model download |
| AI | Claude Haiku (answer generation with mandatory citation system prompt) |
| Storage | SQLite (Document + Chunk tables, denormalized) |
| Frontend | Jinja2 templates + vanilla CSS |
| Deploy | Render (DEMO_MODE=False — always calls Claude with pre-seeded corpus) |

---

## Quick Start

```bash
git clone https://github.com/JakPot42/civic-rag.git
cd civic-rag
cp .env.example .env          # add ANTHROPIC_API_KEY=sk-ant-...
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\uvicorn main:app --reload
```

Open http://localhost:8000

---

## Example Queries

```
"What did the town council decide about the Crandall Road property?"
→ [Town Council, May 2024]: Voted 4-1 to approve acquisition of 55 acres for open space...

"What is the current school budget?"
→ [School Committee, April 2024]: The FY2024 school budget was set at $X million...

"Was the Stafford Road development approved?"
→ [Planning Board, April 2024]: The Planning Board denied the application for multi-family...

"What is the town's stance on new nuclear plants?"
→ Not found in the indexed Tiverton meeting documents.
```

The last response is the correct behavior — the system does not speculate.

---

## Architecture

```
rag.py          BM25Index class: document indexing, IDF computation, BM25 scoring (k1=1.5, b=0.75)
search.py       Query pipeline: BM25 retrieve top-K chunks → build context → Claude answer with citation prompt
models.py       SQLAlchemy ORM (Document, Chunk) — denormalized for fast retrieval
seed_data.py    7 Tiverton 2024 meeting documents, pre-chunked with governing body and date metadata
main.py         FastAPI routes (search, document list, about), Jinja rendering, lifespan seed
config.py       DEMO_MODE, BM25 parameters, chunk size, top-K
```

---

## Key Architecture Decisions

**Why BM25 over vector embeddings:**
The corpus is hyperlocal civic text — "Stafford Road," "Crandall Road," "FY2024 budget allocation." BM25 retrieves these keyword matches reliably without a sentence-transformer model download (60–500 MB depending on the model) or an ONNX runtime. Same decision as Portfolio RAG and for the same reason: keyword-heavy technical text where BM25 is competitive with or better than cosine similarity on sparse corpora.

**Why mandatory citations:**
Civic information is high-stakes for residents. Claiming "the council approved X" without a source is the same problem as hallucinated legal citations in Citation Checker. The citation system prompt in every Claude call enforces `[Governing Body, Date]` attribution for every claim — the user can verify against the source document.

**Why Tiverton, RI:**
A real place with real stakes, close enough to be personally accountable for accuracy. Pre-seeded with real documents rather than scraped live — same discipline as GhostTrace using cached EDGAR filings rather than live queries. Reproducible, inspectable, no rate-limit surprises.

**DEMO_MODE=False:**
Unlike most portfolio projects, Civic RAG always calls Claude — the retrieval and answer generation are inseparable. The corpus is small enough (19 chunks) that every query is fast and cheap.

---

## Honest Limitations

- Scoped to Tiverton, RI, 2024. Extending to other municipalities requires adding their meeting documents to the corpus.
- 7 documents / 19 chunks is a small corpus. Questions about topics not covered by the seeded meetings will correctly return "not found."
- BM25 is keyword-matching — paraphrased questions that don't share vocabulary with the document text may return weak results.
- Meeting documents are pre-seeded from real 2024 Tiverton records; they may not reflect more recent decisions.

---

## Tests

```bash
venv\Scripts\python.exe -m pytest tests/ -v
# 49 passed
```

Covers: BM25 indexing (IDF computation, score ranking), citation enforcement (Claude response parsing), chunk metadata integrity, seed data load, FastAPI route responses.

---

*Meeting documents sourced from Tiverton, RI public records. DEMO_MODE=False — this is a live tool, not a demo; all answers are generated by Claude from pre-indexed civic documents.*
