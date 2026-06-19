"""Tests for BM25 keyword search over civic chunks."""
import pytest
from search import tokenize, BM25Index, build_index


# ---------------------------------------------------------------------------
# tokenize()
# ---------------------------------------------------------------------------

def test_tokenize_basic():
    tokens = tokenize("zoning change multi-family housing")
    assert "zoning" in tokens
    assert "housing" in tokens


def test_tokenize_lowercases():
    tokens = tokenize("Town Council Budget")
    assert "town" in tokens
    assert "council" in tokens
    assert "budget" in tokens


def test_tokenize_removes_stop_words():
    tokens = tokenize("a the is and or")
    assert tokens == []


def test_tokenize_empty():
    assert tokenize("") == []


def test_tokenize_numbers_excluded():
    # Regex is [a-z]+ so digits are not captured
    tokens = tokenize("rate 13.72 per 1000")
    assert "13" not in tokens
    assert "rate" in tokens
    assert "per" not in tokens  # stop word


# ---------------------------------------------------------------------------
# BM25Index construction
# ---------------------------------------------------------------------------

def _make_chunks(bodies: list[str]) -> list[dict]:
    return [
        {
            "chunk_id": i,
            "document_id": 1,
            "heading": "",
            "body": b,
            "municipality": "Tiverton",
            "governing_body": "Town Council",
            "meeting_date": "2024-01-01",
            "doc_title": "Test Doc",
            "source_url": "",
        }
        for i, b in enumerate(bodies)
    ]


def test_bm25_index_builds_without_error():
    chunks = _make_chunks(["zoning housing development", "school budget teachers"])
    idx = BM25Index(chunks)
    assert idx is not None


def test_bm25_empty_corpus():
    idx = BM25Index([])
    results = idx.search("zoning")
    assert results == []


def test_bm25_empty_query_returns_empty():
    chunks = _make_chunks(["zoning housing development"])
    idx = BM25Index(chunks)
    assert idx.search("") == []
    assert idx.search("   ") == []


def test_bm25_scores_relevant_doc_higher():
    chunks = _make_chunks([
        "zoning housing development multi-family residential apartment permit",
        "school budget teachers salaries contract union ratification",
    ])
    idx = BM25Index(chunks)
    results = idx.search("multi-family housing zoning", top_k=2)
    assert len(results) >= 1
    # First result should be the zoning doc
    assert "zoning" in results[0]["body"] or "housing" in results[0]["body"]


def test_bm25_top_k_limits_results():
    chunks = _make_chunks([
        "budget tax rate property levy",
        "budget appropriation fiscal year increase",
        "budget committee vote finance approval",
        "road paving highway maintenance asphalt",
    ])
    idx = BM25Index(chunks)
    results = idx.search("budget fiscal year", top_k=2)
    assert len(results) <= 2


def test_bm25_no_matches_returns_empty():
    chunks = _make_chunks(["school budget teachers", "road paving highway"])
    idx = BM25Index(chunks)
    # Query with only stop words and unknown tokens
    results = idx.search("zzz xyzzy quux", top_k=5)
    assert results == []


def test_bm25_returns_chunk_dicts():
    chunks = _make_chunks(["zoning housing development"])
    idx = BM25Index(chunks)
    results = idx.search("zoning")
    assert len(results) == 1
    assert "body" in results[0]
    assert "municipality" in results[0]
    assert "governing_body" in results[0]
    assert "meeting_date" in results[0]


def test_bm25_single_chunk_corpus():
    chunks = _make_chunks(["the town council adopted the FY2025 budget"])
    idx = BM25Index(chunks)
    results = idx.search("council budget")
    assert len(results) == 1


def test_build_index_returns_bm25_index():
    chunks = _make_chunks(["test document content"])
    idx = build_index(chunks)
    assert isinstance(idx, BM25Index)


# ---------------------------------------------------------------------------
# Realistic civic queries
# ---------------------------------------------------------------------------

CIVIC_CHUNKS = _make_chunks([
    (
        "The Planning Board voted 4-1 to deny the special use permit for a 12-unit "
        "multi-family residential development on Stafford Road due to sewer capacity."
    ),
    (
        "The council set the FY2025 property tax rate at $13.72 per $1,000 of assessed value, "
        "up from $13.28 in FY2024."
    ),
    (
        "The committee approved the STEM curriculum expansion including computer science "
        "courses at Tiverton Middle School and Tiverton High School."
    ),
    (
        "Highway Superintendent Raposa presented the road paving schedule covering 8.3 miles "
        "including Neck Road, Brayton Road, and Indian Town Road."
    ),
    (
        "The council authorized the purchase of a 55-acre open space parcel on Crandall Road "
        "for $1.1 million from the Open Space Acquisition Fund."
    ),
])


def test_civic_zoning_query_finds_planning_chunk():
    idx = build_index(CIVIC_CHUNKS)
    results = idx.search("multi-family housing zoning development")
    assert any("Stafford" in r["body"] or "multi-family" in r["body"] for r in results)


def test_civic_tax_query_finds_tax_chunk():
    idx = build_index(CIVIC_CHUNKS)
    results = idx.search("property tax rate assessed value")
    assert any("tax" in r["body"] for r in results)


def test_civic_school_query_finds_stem_chunk():
    idx = build_index(CIVIC_CHUNKS)
    results = idx.search("school curriculum computer science")
    assert any("STEM" in r["body"] or "computer" in r["body"] for r in results)


def test_civic_road_query_finds_paving_chunk():
    idx = build_index(CIVIC_CHUNKS)
    results = idx.search("road paving maintenance schedule")
    assert any("paving" in r["body"] or "Road" in r["body"] for r in results)


def test_civic_open_space_query():
    idx = build_index(CIVIC_CHUNKS)
    results = idx.search("open space conservation land purchase")
    assert any("open space" in r["body"].lower() or "Crandall" in r["body"] for r in results)
