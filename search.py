"""Pure-Python BM25 retrieval over meeting minute chunks — no external deps."""
import math
import re
from collections import Counter
from dataclasses import dataclass, field


_STOP_WORDS = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "as", "this", "that", "these",
    "those", "it", "its", "and", "or", "but", "not", "no", "all",
    "any", "each", "which", "who", "what", "when", "where", "how",
    "per", "up", "out", "into", "than", "over", "under", "about",
})


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\b[a-z]+\b", text.lower())
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 1]


@dataclass
class SearchResult:
    chunk: dict
    score: float


class BM25Index:
    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self._chunks = chunks
        self.k1 = k1
        self.b = b
        self._tokenized = [tokenize(c["heading"] + " " + c["body"]) for c in chunks]
        n = len(chunks)
        self._avgdl = sum(len(d) for d in self._tokenized) / max(n, 1)

        df: Counter = Counter()
        for doc_tokens in self._tokenized:
            for term in set(doc_tokens):
                df[term] += 1

        self._idf: dict[str, float] = {
            term: math.log((n - freq + 0.5) / (freq + 0.5) + 1)
            for term, freq in df.items()
        }

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_terms = tokenize(query)
        if not query_terms:
            return []

        scores: list[tuple[int, float]] = []
        for idx, doc_tokens in enumerate(self._tokenized):
            dl = len(doc_tokens)
            tf = Counter(doc_tokens)
            score = 0.0
            for term in query_terms:
                if term not in self._idf:
                    continue
                tf_val = tf[term]
                numerator = tf_val * (self.k1 + 1)
                denominator = tf_val + self.k1 * (
                    1 - self.b + self.b * dl / max(self._avgdl, 1)
                )
                score += self._idf[term] * numerator / denominator
            if score > 0:
                scores.append((idx, score))

        scores.sort(key=lambda x: -x[1])
        return [self._chunks[idx] for idx, _ in scores[:top_k]]


def build_index(chunks: list[dict]) -> BM25Index:
    return BM25Index(chunks)
