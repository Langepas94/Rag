import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import numpy as np

from .chunking import fixed_chunk_documents, structural_chunk_documents
from .embeddings import Embedder
from .loaders import estimate_page_count, load_documents
from .models import Chunk
from .vector_store import VectorIndex, save_index


def build_index(
    corpus_dir: Path,
    out_root: Path,
    strategy: str,
    embedder: Embedder,
    fixed_chars: int = 1200,
    fixed_overlap: int = 180,
    structural_max_chars: int = 1800,
    structural_overlap: int = 160,
) -> Dict[str, Any]:
    documents = load_documents(corpus_dir)
    if not documents:
        raise RuntimeError("No supported documents found in %s" % corpus_dir)

    if strategy == "fixed":
        chunks = fixed_chunk_documents(documents, max_chars=fixed_chars, overlap=fixed_overlap)
        chunk_settings = {"max_chars": fixed_chars, "overlap": fixed_overlap}
    elif strategy == "structural":
        chunks = structural_chunk_documents(documents, max_chars=structural_max_chars, overlap=structural_overlap)
        chunk_settings = {"max_chars": structural_max_chars, "overlap": structural_overlap}
    else:
        raise ValueError("Unknown strategy: %s" % strategy)

    if not chunks:
        raise RuntimeError("No chunks were produced for %s" % corpus_dir)

    vectors = embedder.embed([chunk.text for chunk in chunks])
    manifest = {
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "strategy": strategy,
        "embedder": embedder.name,
        "model": getattr(embedder, "model", None),
        "corpus_dir": str(corpus_dir),
        "document_count": len(documents),
        "estimated_pages": round(estimate_page_count(documents), 2),
        "text_characters": sum(len(doc.text) for doc in documents),
        "chunk_settings": chunk_settings,
        "stats": chunk_stats(chunks),
    }
    index_dir = out_root / strategy
    final_manifest = save_index(index_dir, chunks, vectors, manifest)
    return final_manifest


def chunk_stats(chunks: Sequence[Chunk]) -> Dict[str, Any]:
    lengths = [len(chunk.text) for chunk in chunks]
    token_estimates = [int(chunk.metadata.get("token_estimate", 0)) for chunk in chunks]
    source_counts = Counter(chunk.source for chunk in chunks)
    sections = [chunk.section for chunk in chunks if chunk.section]
    return {
        "chunks": len(chunks),
        "avg_chars": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "min_chars": min(lengths) if lengths else 0,
        "max_chars": max(lengths) if lengths else 0,
        "avg_tokens_estimate": round(sum(token_estimates) / len(token_estimates), 2) if token_estimates else 0,
        "with_section": len(sections),
        "with_section_ratio": round(len(sections) / float(len(chunks)), 3) if chunks else 0,
        "chunks_per_source": dict(sorted(source_counts.items())),
    }


def compare_indexes(
    index_root: Path,
    strategies: Sequence[str],
    embedder: Embedder,
    queries_path: Optional[Path] = None,
    top_k: int = 5,
    search_mode: str = "dense",
) -> Dict[str, Any]:
    indexes = {strategy: VectorIndex(index_root / strategy) for strategy in strategies}
    report: Dict[str, Any] = {
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "search_mode": search_mode,
        "strategies": {},
    }
    for strategy, index in indexes.items():
        report["strategies"][strategy] = {
            "manifest": index.manifest,
            "stats": index.manifest.get("stats", {}),
        }

    if queries_path:
        queries = load_queries(queries_path)
        for strategy, index in indexes.items():
            report["strategies"][strategy]["retrieval"] = evaluate_index(index, embedder, queries, top_k=top_k, search_mode=search_mode)
        report["queries"] = queries

    return report


def load_queries(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, dict):
        payload = payload.get("queries", [])
    if not isinstance(payload, list):
        raise ValueError("Query file must contain a list or {'queries': [...]}")
    return payload


def evaluate_index(
    index: VectorIndex,
    embedder: Embedder,
    queries: Sequence[Dict[str, Any]],
    top_k: int = 5,
    search_mode: str = "hybrid",
) -> Dict[str, Any]:
    if not queries:
        return {}
    search_k = max(top_k, 5)
    rows = []
    for query in queries:
        vector = embedder.embed([query["query"]])
        results = index.search(vector, top_k=search_k, mode=search_mode, query_text=query["query"])
        rows.append(evaluate_query(query, results))

    return {
        "query_count": len(rows),
        "source_hit_at_1": average(row["source_hit_at_1"] for row in rows),
        "source_hit_at_3": average(row["source_hit_at_3"] for row in rows),
        "source_hit_at_5": average(row["source_hit_at_5"] for row in rows),
        "section_hit_at_1": average(row["section_hit_at_1"] for row in rows if row["has_expected_section"]),
        "section_hit_at_3": average(row["section_hit_at_3"] for row in rows if row["has_expected_section"]),
        "section_hit_at_5": average(row["section_hit_at_5"] for row in rows if row["has_expected_section"]),
        "mrr_source": average(row["mrr_source"] for row in rows),
        "rows": rows,
    }


def evaluate_query(query: Dict[str, Any], results: Sequence[Any]) -> Dict[str, Any]:
    expected_sources = expected_values(query, "expected_source", "expected_sources")
    expected_sections = expected_values(query, "expected_section", "expected_sections")
    source_ranks = [
        rank
        for rank, result in enumerate(results, start=1)
        if expected_sources and any(source_matches(str(result.chunk.get("source")), expected) for expected in expected_sources)
    ]
    section_ranks = [
        rank
        for rank, result in enumerate(results, start=1)
        if expected_sections and any(section_matches(str(result.chunk.get("section")), expected) for expected in expected_sections)
    ]
    return {
        "query": query["query"],
        "expected_sources": expected_sources,
        "expected_sections": expected_sections,
        "source_rank": source_ranks[0] if source_ranks else None,
        "section_rank": section_ranks[0] if section_ranks else None,
        "source_hit_at_1": 1 if source_ranks and source_ranks[0] <= 1 else 0,
        "source_hit_at_3": 1 if source_ranks and source_ranks[0] <= 3 else 0,
        "source_hit_at_5": 1 if source_ranks and source_ranks[0] <= 5 else 0,
        "section_hit_at_1": 1 if section_ranks and section_ranks[0] <= 1 else 0,
        "section_hit_at_3": 1 if section_ranks and section_ranks[0] <= 3 else 0,
        "section_hit_at_5": 1 if section_ranks and section_ranks[0] <= 5 else 0,
        "has_expected_section": bool(expected_sections),
        "mrr_source": 1.0 / source_ranks[0] if source_ranks else 0.0,
        "top_results": [
            {
                "rank": rank,
                "score": round(float(result.score), 4),
                "dense_score": round(float(getattr(result, "dense_score", result.score)), 4),
                "lexical_score": round(float(getattr(result, "lexical_score", 0.0) or 0.0), 4),
                "source": result.chunk.get("source"),
                "section": result.chunk.get("section"),
                "chunk_id": result.chunk.get("chunk_id"),
            }
            for rank, result in enumerate(results[:5], start=1)
        ],
    }


def source_matches(actual: str, expected: str) -> bool:
    return actual == expected or actual.endswith(expected) or expected in actual


def section_matches(actual: str, expected: str) -> bool:
    return expected.lower() in actual.lower() or actual.lower() in expected.lower()


def expected_values(query: Dict[str, Any], single_key: str, list_key: str) -> List[str]:
    values = query.get(list_key)
    if values is None:
        values = query.get(single_key)
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    return [str(value) for value in values]


def average(values: Iterable[float]) -> Optional[float]:
    items = list(values)
    if not items:
        return None
    return round(sum(items) / float(len(items)), 4)


def render_markdown_report(report: Dict[str, Any]) -> str:
    lines = ["# Chunking Strategy Comparison", ""]
    lines.append("Generated at: `%s`" % report.get("created_at", ""))
    lines.append("Search mode: `%s`" % report.get("search_mode", "dense"))
    lines.append("")
    lines.append("## Chunk Statistics")
    lines.append("")
    lines.append("| Strategy | Chunks | Avg chars | Min | Max | Section coverage | Backend |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for strategy, data in report["strategies"].items():
        manifest = data["manifest"]
        stats = data["stats"]
        lines.append(
            "| %s | %s | %s | %s | %s | %s | %s |"
            % (
                strategy,
                stats.get("chunks"),
                stats.get("avg_chars"),
                stats.get("min_chars"),
                stats.get("max_chars"),
                stats.get("with_section_ratio"),
                manifest.get("backend"),
            )
        )
    lines.append("")

    if any("retrieval" in data for data in report["strategies"].values()):
        lines.append("## Retrieval Metrics")
        lines.append("")
        lines.append("| Strategy | Queries | hit@1 | hit@3 | hit@5 | section@3 | MRR |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for strategy, data in report["strategies"].items():
            metrics = data.get("retrieval", {})
            lines.append(
                "| %s | %s | %s | %s | %s | %s | %s |"
                % (
                    strategy,
                    metrics.get("query_count"),
                    metrics.get("source_hit_at_1"),
                    metrics.get("source_hit_at_3"),
                    metrics.get("source_hit_at_5"),
                    metrics.get("section_hit_at_3"),
                    metrics.get("mrr_source"),
                )
            )
        lines.append("")
        lines.append("## Query Details")
        lines.append("")
        for strategy, data in report["strategies"].items():
            lines.append("### %s" % strategy)
            lines.append("")
            for row in data.get("retrieval", {}).get("rows", []):
                lines.append("- `%s` -> source rank: `%s`, section rank: `%s`" % (row["query"], row["source_rank"], row["section_rank"]))
                if row["top_results"]:
                    top = row["top_results"][0]
                    lines.append(
                        "  - top1: `%s` / `%s` score `%s` dense `%s` lexical `%s`"
                        % (top["source"], top["section"], top["score"], top.get("dense_score"), top.get("lexical_score"))
                    )
            lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- Fixed chunking is expected to produce more uniform chunk sizes and predictable overlap.")
    lines.append("- Structural chunking is expected to preserve headings, pages, functions, and sections more often.")
    lines.append("- Prefer the strategy with stronger retrieval metrics unless its chunk sizes are too uneven for the target context window.")
    lines.append("")
    return "\n".join(lines)
