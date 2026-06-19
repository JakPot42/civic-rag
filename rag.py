"""RAG module: retrieve chunks → Claude answers with strict citation discipline."""
import json

import anthropic

from config import DEMO_MODE, ANTHROPIC_API_KEY, CLAUDE_MODEL

_SYSTEM_PROMPT = """\
You are a civic information assistant for Tiverton, Rhode Island.

You have been given excerpts from official meeting minutes and agendas. Answer the user's \
question using ONLY this provided context.

CITATION RULES — mandatory for every response:
- For every factual claim, include a citation in this exact format: \
[Tiverton {Governing Body}, {Date}]
- Example: "The council set the tax rate at $13.72 per $1,000 [Tiverton Town Council, May 6, 2024]."
- If multiple sources support a claim, cite all of them.
- If the answer is not in the provided context, say exactly: \
"The available meeting records do not contain information about this topic."
- Never speculate or draw on knowledge outside the provided documents.
- Be concise and direct."""

_DEMO_ANSWER = """\
Based on the available meeting records, there have been several notable zoning and housing \
developments in Tiverton in 2024.

The Planning Board denied a special use permit for a 12-unit multi-family development on \
Stafford Road, finding that the existing sewer main lacks adequate capacity and the Pine Hill \
Road pump station would require a $340,000 upgrade before the development could be occupied \
[Tiverton Planning Board, March 20, 2024]. The applicant indicated an intent to appeal to the \
Zoning Board of Review.

Separately, the Planning Board reviewed a proposed rezoning of the Highland Road corridor from \
R-10 (10,000 sq ft minimum lot size) to R-20 (20,000 sq ft minimum), which would reduce \
allowable density. Initiated by 47 residents, the amendment was not voted on — the board \
scheduled a public hearing for April 17, 2024 before making a recommendation to the Town Council \
[Tiverton Planning Board, March 20, 2024].

On the conservation side, the Town Council authorized — and subsequently completed — the purchase \
of a 55-acre parcel on Crandall Road for $1.1 million from the Open Space Fund, permanently \
protecting it from residential or commercial development under a conservation restriction held by \
the Tiverton Land Trust [Tiverton Town Council, March 11, 2024; Tiverton Town Council, June 10, \
2024].

The available meeting records do not contain information about any approved multi-family \
developments or additional pending zoning changes beyond those described above."""

_DEMO_SOURCES = [
    {
        "chunk_id": 0,
        "document_id": 6,
        "heading": "Special Use Permit Denied — Stafford Road Multi-Family Development",
        "body": (
            "The Planning Board voted 4-1 to deny the special use permit application submitted by "
            "Harbor View Development LLC for a 12-unit multi-family residential complex..."
        ),
        "municipality": "Tiverton",
        "governing_body": "Planning Board",
        "meeting_date": "2024-03-20",
        "doc_title": "Planning Board Regular Meeting Minutes — March 20, 2024",
        "source_url": "https://www.tiverton.ri.gov/planning-board/minutes",
    },
    {
        "chunk_id": 0,
        "document_id": 6,
        "heading": "Zoning Text Amendment — Highland Road Corridor Rezoning",
        "body": (
            "The board continued its review of a proposed zoning text amendment that would rezone "
            "the Highland Road corridor from R-10 to R-20..."
        ),
        "municipality": "Tiverton",
        "governing_body": "Planning Board",
        "meeting_date": "2024-03-20",
        "doc_title": "Planning Board Regular Meeting Minutes — March 20, 2024",
        "source_url": "https://www.tiverton.ri.gov/planning-board/minutes",
    },
    {
        "chunk_id": 0,
        "document_id": 1,
        "heading": "Open Space Land Purchase — Crandall Road Parcel",
        "body": (
            "The council voted 4-1 to authorize the purchase of a 55-acre undeveloped parcel on "
            "Crandall Road from the Machado family trust for $1.1 million..."
        ),
        "municipality": "Tiverton",
        "governing_body": "Town Council",
        "meeting_date": "2024-03-11",
        "doc_title": "Town Council Regular Meeting Minutes — March 11, 2024",
        "source_url": "https://www.tiverton.ri.gov/town-council/minutes",
    },
]


def _format_context(chunks: list[dict]) -> str:
    if not chunks:
        return "(No relevant records found.)"
    parts = []
    for i, c in enumerate(chunks, 1):
        citation = f"[Tiverton {c['governing_body']}, {c['meeting_date']}]"
        parts.append(
            f"SOURCE {i} — {citation}\n"
            f"Heading: {c['heading']}\n"
            f"{c['body']}"
        )
    return "\n\n---\n\n".join(parts)


def ask(question: str, chunks: list[dict], client=None) -> dict:
    """Return {"answer": str, "sources": list[dict]}."""
    if DEMO_MODE:
        return {"answer": _DEMO_ANSWER, "sources": _DEMO_SOURCES}

    context = _format_context(chunks)
    user_message = f"Context from Tiverton meeting records:\n\n{context}\n\nQuestion: {question}"

    if client is None:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        answer = response.content[0].text
    except Exception as exc:
        answer = (
            f"Unable to generate an answer at this time. Error: {exc}\n\n"
            "The source records retrieved are shown below."
        )

    return {"answer": answer, "sources": chunks}
