"""Tests for rag.py — format_context, DEMO_MODE behavior, ask() contract."""
import os
import pytest

# Force DEMO_MODE for all tests — no real Claude calls
os.environ["DEMO_MODE"] = "True"

import rag
from rag import _format_context, _SYSTEM_PROMPT, _DEMO_ANSWER, _DEMO_SOURCES, ask


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_chunk(
    governing_body="Town Council",
    meeting_date="2024-05-06",
    heading="Budget Adoption",
    body="The council adopted the FY2025 budget of $18.4 million.",
    municipality="Tiverton",
    document_id=1,
) -> dict:
    return {
        "chunk_id": 1,
        "document_id": document_id,
        "heading": heading,
        "body": body,
        "municipality": municipality,
        "governing_body": governing_body,
        "meeting_date": meeting_date,
        "doc_title": "Town Council Minutes",
        "source_url": "https://www.tiverton.ri.gov/town-council/minutes",
    }


# ---------------------------------------------------------------------------
# _format_context()
# ---------------------------------------------------------------------------

def test_format_context_empty_returns_placeholder():
    result = _format_context([])
    assert "No relevant records" in result


def test_format_context_single_chunk_contains_body():
    chunk = _make_chunk(body="The council adopted the FY2025 budget.")
    result = _format_context([chunk])
    assert "FY2025 budget" in result


def test_format_context_single_chunk_contains_citation():
    chunk = _make_chunk(governing_body="Town Council", meeting_date="2024-05-06")
    result = _format_context([chunk])
    assert "Town Council" in result
    assert "2024-05-06" in result


def test_format_context_single_chunk_contains_heading():
    chunk = _make_chunk(heading="Tax Rate Discussion")
    result = _format_context([chunk])
    assert "Tax Rate Discussion" in result


def test_format_context_multiple_chunks_has_separator():
    chunks = [_make_chunk(), _make_chunk(heading="Second Item")]
    result = _format_context(chunks)
    assert "---" in result


def test_format_context_multiple_chunks_source_numbering():
    chunks = [_make_chunk(), _make_chunk()]
    result = _format_context(chunks)
    assert "SOURCE 1" in result
    assert "SOURCE 2" in result


def test_format_context_includes_planning_board():
    chunk = _make_chunk(governing_body="Planning Board", meeting_date="2024-03-20")
    result = _format_context([chunk])
    assert "Planning Board" in result
    assert "2024-03-20" in result


def test_format_context_includes_school_committee():
    chunk = _make_chunk(governing_body="School Committee", meeting_date="2024-02-12")
    result = _format_context([chunk])
    assert "School Committee" in result


# ---------------------------------------------------------------------------
# System prompt content
# ---------------------------------------------------------------------------

def test_system_prompt_contains_citation_instruction():
    assert "citation" in _SYSTEM_PROMPT.lower() or "cite" in _SYSTEM_PROMPT.lower()


def test_system_prompt_contains_tiverton():
    assert "Tiverton" in _SYSTEM_PROMPT


def test_system_prompt_contains_only_context_rule():
    assert "ONLY" in _SYSTEM_PROMPT


def test_system_prompt_contains_dont_know_instruction():
    assert "do not contain" in _SYSTEM_PROMPT or "don't know" in _SYSTEM_PROMPT.lower()


# ---------------------------------------------------------------------------
# DEMO_MODE behavior of ask()
# ---------------------------------------------------------------------------

def test_ask_demo_mode_returns_dict():
    result = ask("any question", [])
    assert isinstance(result, dict)


def test_ask_demo_mode_has_answer_key():
    result = ask("any question", [])
    assert "answer" in result


def test_ask_demo_mode_has_sources_key():
    result = ask("any question", [])
    assert "sources" in result


def test_ask_demo_mode_answer_is_string():
    result = ask("any question", [])
    assert isinstance(result["answer"], str)


def test_ask_demo_mode_answer_nonempty():
    result = ask("any question", [])
    assert len(result["answer"]) > 50


def test_ask_demo_mode_sources_is_list():
    result = ask("any question", [])
    assert isinstance(result["sources"], list)


def test_ask_demo_mode_returns_prebaked_answer():
    result = ask("any question", [])
    assert result["answer"] == _DEMO_ANSWER


def test_ask_demo_mode_returns_prebaked_sources():
    result = ask("any question", [])
    assert result["sources"] == _DEMO_SOURCES


def test_ask_demo_mode_ignores_passed_chunks():
    chunk = _make_chunk(body="This chunk should be ignored in demo mode.")
    result = ask("any question", [chunk])
    # Demo mode always returns pre-baked, not the passed chunks
    assert result["answer"] == _DEMO_ANSWER


def test_ask_demo_mode_ignores_question():
    result1 = ask("question one", [])
    result2 = ask("question two about schools", [])
    assert result1["answer"] == result2["answer"]


# ---------------------------------------------------------------------------
# DEMO_MODE source structure
# ---------------------------------------------------------------------------

def test_demo_sources_are_nonempty():
    assert len(_DEMO_SOURCES) > 0


def test_demo_sources_each_has_heading():
    for src in _DEMO_SOURCES:
        assert "heading" in src
        assert len(src["heading"]) > 0


def test_demo_sources_each_has_governing_body():
    for src in _DEMO_SOURCES:
        assert "governing_body" in src


def test_demo_sources_each_has_meeting_date():
    for src in _DEMO_SOURCES:
        assert "meeting_date" in src
        assert len(src["meeting_date"]) == 10  # YYYY-MM-DD


def test_demo_sources_each_has_body():
    for src in _DEMO_SOURCES:
        assert "body" in src
        assert len(src["body"]) > 20


def test_demo_answer_contains_tiverton_citation():
    assert "[Tiverton" in _DEMO_ANSWER


def test_demo_answer_contains_planning_board_citation():
    assert "Planning Board" in _DEMO_ANSWER


def test_demo_answer_contains_town_council_citation():
    assert "Town Council" in _DEMO_ANSWER
