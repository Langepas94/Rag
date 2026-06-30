import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence

import requests

from .embeddings import Embedder
from .vector_store import SearchResult, VectorIndex


DEFAULT_SYSTEM_PROMPT = (
    "You are a precise assistant. Answer in the user's language. "
    "When context sources are provided, use them as the primary evidence. "
    "If the context is insufficient, say what is missing instead of inventing details."
)


class ChatClient(Protocol):
    def complete(self, messages: Sequence[Dict[str, str]]) -> str:
        ...


class OllamaChatClient:
    def __init__(
        self,
        model: str = "qwen2.5:7b",
        base_url: str = "http://localhost:11434",
        timeout: int = 180,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def complete(self, messages: Sequence[Dict[str, str]]) -> str:
        try:
            response = requests.post(
                "%s/api/chat" % self.base_url,
                json={"model": self.model, "messages": list(messages), "stream": False},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise RuntimeError(
                "Could not reach Ollama chat at %s. Start Ollama and pull the model '%s'."
                % (self.base_url, self.model)
            ) from exc
        response.raise_for_status()
        payload = response.json()
        content = payload.get("message", {}).get("content")
        if content is None:
            raise RuntimeError("Ollama response did not contain message.content")
        return str(content).strip()


@dataclass
class AgentAnswer:
    mode: str
    question: str
    answer: str
    sources: List[Dict[str, Any]]

    def to_json(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "question": self.question,
            "answer": self.answer,
            "sources": self.sources,
        }


class RagAgent:
    def __init__(
        self,
        chat_client: ChatClient,
        embedder: Embedder,
        index: Optional[VectorIndex] = None,
        top_k: int = 5,
        search_mode: str = "hybrid",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        max_context_chars: int = 8000,
    ) -> None:
        self.chat_client = chat_client
        self.embedder = embedder
        self.index = index
        self.top_k = top_k
        self.search_mode = search_mode
        self.system_prompt = system_prompt
        self.max_context_chars = max_context_chars

    def answer(self, question: str, use_rag: bool = True) -> AgentAnswer:
        sources: List[Dict[str, Any]] = []
        user_content = question
        if use_rag:
            if self.index is None:
                raise RuntimeError("RAG mode requires an index")
            results = retrieve_chunks(
                self.index,
                self.embedder,
                question,
                top_k=self.top_k,
                search_mode=self.search_mode,
            )
            sources = [source_from_result(result, rank) for rank, result in enumerate(results, start=1)]
            user_content = build_rag_user_message(question, results, self.max_context_chars)

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_content},
        ]
        mode = "rag" if use_rag else "plain"
        return AgentAnswer(mode=mode, question=question, answer=self.chat_client.complete(messages), sources=sources)

    def compare(self, question: str) -> Dict[str, Any]:
        plain = self.answer(question, use_rag=False)
        rag = self.answer(question, use_rag=True)
        return {
            "question": question,
            "plain": plain.to_json(),
            "rag": rag.to_json(),
        }


def retrieve_chunks(
    index: VectorIndex,
    embedder: Embedder,
    question: str,
    top_k: int = 5,
    search_mode: str = "hybrid",
) -> List[SearchResult]:
    vector = embedder.embed([question])
    return index.search(vector, top_k=top_k, mode=search_mode, query_text=question)


def build_rag_user_message(question: str, results: Sequence[SearchResult], max_context_chars: int = 8000) -> str:
    context_blocks: List[str] = []
    remaining = max_context_chars
    for rank, result in enumerate(results, start=1):
        chunk = result.chunk
        header = "[%d] source=%s section=%s chunk_id=%s" % (
            rank,
            chunk.get("source", ""),
            chunk.get("section", ""),
            chunk.get("chunk_id", ""),
        )
        text = str(chunk.get("text", "")).strip()
        block = "%s\n%s" % (header, text)
        if len(block) > remaining:
            block = block[: max(0, remaining)].rstrip()
        if block:
            context_blocks.append(block)
            remaining -= len(block)
        if remaining <= 0:
            break

    return (
        "Question:\n%s\n\n"
        "Retrieved context:\n%s\n\n"
        "Answer using the retrieved context. Cite source paths in prose when they matter."
        % (question, "\n\n---\n\n".join(context_blocks))
    )


def source_from_result(result: SearchResult, rank: int) -> Dict[str, Any]:
    chunk = result.chunk
    return {
        "rank": rank,
        "score": round(float(result.score), 4),
        "dense_score": round(float(result.dense_score), 4),
        "lexical_score": round(float(result.lexical_score or 0.0), 4),
        "source": chunk.get("source"),
        "section": chunk.get("section"),
        "chunk_id": chunk.get("chunk_id"),
    }


def evaluate_answers(
    agent: RagAgent,
    questions: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    rows = []
    for item in questions:
        comparison = agent.compare(str(item["query"]))
        row = evaluate_answer_pair(item, comparison)
        rows.append(row)

    return {
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "question_count": len(rows),
        "summary": {
            "rag_source_hit_at_5": average(row["rag"]["source_hit_at_5"] for row in rows),
            "plain_expectation_coverage": average(row["plain"]["expectation_coverage"] for row in rows),
            "rag_expectation_coverage": average(row["rag"]["expectation_coverage"] for row in rows),
        },
        "rows": rows,
    }


def evaluate_answer_pair(question: Dict[str, Any], comparison: Dict[str, Any]) -> Dict[str, Any]:
    expected_sources = expected_values(question, "expected_source", "expected_sources")
    expected_contains = expected_contains_values(question)
    plain = comparison["plain"]
    rag = comparison["rag"]
    return {
        "query": question["query"],
        "expectation": question.get("expectation", ""),
        "expected_sources": expected_sources,
        "plain": answer_metrics(plain, expected_sources, expected_contains),
        "rag": answer_metrics(rag, expected_sources, expected_contains),
        "plain_answer": plain["answer"],
        "rag_answer": rag["answer"],
        "rag_sources": rag["sources"],
    }


def answer_metrics(answer_payload: Dict[str, Any], expected_sources: Sequence[str], expected_contains: Sequence[str]) -> Dict[str, Any]:
    answer = str(answer_payload.get("answer", ""))
    used_sources = [str(source.get("source", "")) for source in answer_payload.get("sources", [])]
    source_hit = any(source_matches(actual, expected) for actual in used_sources for expected in expected_sources)
    return {
        "source_hit_at_5": 1 if source_hit else 0,
        "expectation_coverage": expectation_coverage(answer, expected_contains),
        "matched_expectations": [item for item in expected_contains if contains_text(answer, item)],
    }


def expected_contains_values(question: Dict[str, Any]) -> List[str]:
    values = question.get("expected_contains")
    if values is None:
        expectation = str(question.get("expectation", ""))
        return [token for token in re.findall(r"[A-Za-zА-Яа-я0-9_./-]{4,}", expectation)[:8]]
    if isinstance(values, str):
        return [values]
    return [str(value) for value in values]


def expectation_coverage(answer: str, expected_contains: Sequence[str]) -> float:
    if not expected_contains:
        return 0.0
    matched = sum(1 for item in expected_contains if contains_text(answer, item))
    return round(matched / float(len(expected_contains)), 4)


def contains_text(answer: str, needle: str) -> bool:
    return needle.lower() in answer.lower()


def expected_values(query: Dict[str, Any], single_key: str, list_key: str) -> List[str]:
    values = query.get(list_key)
    if values is None:
        values = query.get(single_key)
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    return [str(value) for value in values]


def source_matches(actual: str, expected: str) -> bool:
    return actual == expected or actual.endswith(expected) or expected in actual


def average(values: Iterable[float]) -> Optional[float]:
    items = list(values)
    if not items:
        return None
    return round(sum(items) / float(len(items)), 4)


def load_control_questions(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        payload = payload.get("queries", [])
    if not isinstance(payload, list):
        raise ValueError("Control questions file must contain a list or {'queries': [...]}")
    return payload
