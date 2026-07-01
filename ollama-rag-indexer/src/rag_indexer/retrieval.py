import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .embeddings import Embedder
from .vector_store import SearchResult, VectorIndex, tokenize


@dataclass
class RetrievalSettings:
    top_k: int = 5
    candidate_k: Optional[int] = None
    search_mode: str = "hybrid"
    similarity_threshold: Optional[float] = None
    rewrite_query: bool = False

    @property
    def effective_candidate_k(self) -> int:
        if self.candidate_k is None:
            return self.top_k
        return max(self.top_k, self.candidate_k)


@dataclass
class RetrievalTrace:
    original_query: str
    search_query: str
    candidate_count: int
    filtered_count: int
    returned_count: int
    top_k: int
    candidate_k: int
    similarity_threshold: Optional[float]
    rewrite_query: bool

    def to_json(self) -> Dict[str, Any]:
        return {
            "original_query": self.original_query,
            "search_query": self.search_query,
            "candidate_count": self.candidate_count,
            "filtered_count": self.filtered_count,
            "returned_count": self.returned_count,
            "top_k": self.top_k,
            "candidate_k": self.candidate_k,
            "similarity_threshold": self.similarity_threshold,
            "rewrite_query": self.rewrite_query,
        }


def retrieve_with_settings(
    index: VectorIndex,
    embedder: Embedder,
    question: str,
    settings: RetrievalSettings,
) -> List[SearchResult]:
    results, _trace = retrieve_with_trace(index, embedder, question, settings)
    return results


def retrieve_with_trace(
    index: VectorIndex,
    embedder: Embedder,
    question: str,
    settings: RetrievalSettings,
) -> tuple[List[SearchResult], RetrievalTrace]:
    search_query = rewrite_search_query(question) if settings.rewrite_query else question
    vector = None if settings.search_mode == "lexical" else embedder.embed([question])
    candidates = index.search(
        vector,
        top_k=settings.effective_candidate_k,
        mode=settings.search_mode,
        query_text=search_query,
    )
    filtered = filter_relevant(candidates, settings.similarity_threshold)
    results = filtered[: settings.top_k]
    trace = RetrievalTrace(
        original_query=question,
        search_query=search_query,
        candidate_count=len(candidates),
        filtered_count=len(filtered),
        returned_count=len(results),
        top_k=settings.top_k,
        candidate_k=settings.effective_candidate_k,
        similarity_threshold=settings.similarity_threshold,
        rewrite_query=settings.rewrite_query,
    )
    return results, trace


def filter_relevant(results: List[SearchResult], similarity_threshold: Optional[float]) -> List[SearchResult]:
    if similarity_threshold is None:
        return results
    return [result for result in results if float(result.score) >= similarity_threshold]


def rewrite_search_query(query: str) -> str:
    tokens = tokenize(query)
    expansions = []
    for token in tokens:
        expansions.extend(identifier_variants(token))
    expansions.extend(domain_synonyms(tokens))
    unique = []
    seen = set(token.lower() for token in tokens)
    for item in expansions:
        normalized = item.lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique.append(item)
    if not unique:
        return query
    return "%s %s" % (query, " ".join(unique[:24]))


def identifier_variants(token: str) -> List[str]:
    variants = []
    if "_" in token:
        variants.append(token.replace("_", " "))
    if "-" in token:
        variants.append(token.replace("-", " "))
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|[0-9]+", token)
    if len(parts) > 1:
        variants.append(" ".join(parts))
        variants.append("_".join(part.lower() for part in parts))
    return variants


def domain_synonyms(tokens: List[str]) -> List[str]:
    joined = " ".join(tokens)
    expansions = []
    has_telegram = any(token in tokens for token in ["telegram", "tg", "тг", "телеграм", "бот"])
    has_mcp = any(token in tokens for token in ["mcp", "мсп"])
    has_weather = any(token in tokens for token in ["weather", "meteo", "погода", "погоды", "погодный"])
    if has_telegram:
        expansions.extend(["tg-agent", "telegram"])
    if has_mcp and has_telegram:
        expansions.extend(["mcp_client", "connect", "/connect", "stdio", "HTTP"])
    elif has_mcp and has_weather:
        expansions.extend(["open-meteo-mcp"])
    elif has_mcp:
        expansions.extend(["mcp", "mcp_client", "connect", "/connect", "stdio", "HTTP"])
    if has_weather:
        expansions.extend(["open-meteo-mcp", "weather"])
    if any(token in tokens for token in ["trip", "planning", "swarm", "поездка", "путешествие", "планирование"]):
        expansions.extend(["trip", "swarm", "flow", "agent"])
    if any(token in joined for token in ["persist", "персист", "сохран"]) or any(token in tokens for token in ["restart", "sessions", "перезапуск", "сессии"]):
        expansions.extend(["persist", "state", "sessions"])
    return expansions
