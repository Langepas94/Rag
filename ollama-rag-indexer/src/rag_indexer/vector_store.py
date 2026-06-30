import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

from .embeddings import l2_normalize
from .models import Chunk


class SearchResult:
    def __init__(self, chunk: Dict[str, Any], score: float, dense_score: Optional[float] = None, lexical_score: Optional[float] = None) -> None:
        self.chunk = chunk
        self.score = score
        self.dense_score = dense_score if dense_score is not None else score
        self.lexical_score = lexical_score


class VectorIndex:
    def __init__(self, index_dir: Path) -> None:
        self.index_dir = Path(index_dir)
        self.manifest = read_json(self.index_dir / "manifest.json")
        self.chunks = read_jsonl(self.index_dir / "chunks.jsonl")
        self.vectors = np.load(self.index_dir / "vectors.npy").astype(np.float32)
        self.faiss_index = self._load_faiss()
        self._lexical = LexicalIndex(self.chunks)

    def search(self, query_vector: np.ndarray, top_k: int = 5, mode: str = "dense", query_text: Optional[str] = None) -> List[SearchResult]:
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        query_vector = l2_normalize(query_vector.astype(np.float32))
        top_k = min(top_k, len(self.chunks))

        if mode not in {"dense", "hybrid"}:
            raise ValueError("Unknown search mode: %s" % mode)

        dense_scores = self._dense_scores(query_vector)
        if mode == "hybrid" and query_text:
            lexical_scores = self._lexical.scores(query_text)
            combined_scores = combine_scores(dense_scores, lexical_scores)
            indices = np.argsort(-combined_scores)[:top_k]
            return [
                SearchResult(
                    self.chunks[int(index)],
                    float(combined_scores[int(index)]),
                    dense_score=float(dense_scores[int(index)]),
                    lexical_score=float(lexical_scores[int(index)]),
                )
                for index in indices
            ]

        indices = np.argsort(-dense_scores)[:top_k]
        return [SearchResult(self.chunks[int(index)], float(dense_scores[int(index)]), dense_score=float(dense_scores[int(index)])) for index in indices]

    def _dense_scores(self, query_vector: np.ndarray) -> np.ndarray:
        if self.faiss_index is not None:
            scores, indices = self.faiss_index.search(query_vector, len(self.chunks))
            dense_scores = np.full(len(self.chunks), -1.0, dtype=np.float32)
            for score, index in zip(scores[0], indices[0]):
                if int(index) >= 0:
                    dense_scores[int(index)] = float(score)
            return dense_scores

        return np.dot(self.vectors, query_vector[0])

    def _load_faiss(self) -> Optional[Any]:
        faiss_path = self.index_dir / "index.faiss"
        if not faiss_path.exists():
            return None
        try:
            import faiss  # type: ignore
        except ImportError:
            return None
        return faiss.read_index(str(faiss_path))


class LexicalIndex:
    def __init__(self, chunks: List[Dict[str, Any]]) -> None:
        self.documents = [tokenize_search_text(chunk) for chunk in chunks]
        self.term_counts = [Counter(document) for document in self.documents]
        self.lengths = [len(document) for document in self.documents]
        self.avg_len = sum(self.lengths) / float(len(self.lengths)) if self.lengths else 0.0
        self.doc_freq: Counter = Counter()
        for counts in self.term_counts:
            self.doc_freq.update(counts.keys())

    def scores(self, query: str) -> np.ndarray:
        query_terms = tokenize(query)
        if not query_terms or not self.term_counts:
            return np.zeros(len(self.term_counts), dtype=np.float32)

        scores = np.zeros(len(self.term_counts), dtype=np.float32)
        total_docs = len(self.term_counts)
        k1 = 1.5
        b = 0.75
        for term in query_terms:
            df = self.doc_freq.get(term, 0)
            if df == 0:
                continue
            idf = math.log(1.0 + (total_docs - df + 0.5) / (df + 0.5))
            for index, counts in enumerate(self.term_counts):
                tf = counts.get(term, 0)
                if tf == 0:
                    continue
                denom = tf + k1 * (1.0 - b + b * (self.lengths[index] / (self.avg_len or 1.0)))
                scores[index] += idf * ((tf * (k1 + 1.0)) / denom)
        return scores


def combine_scores(dense_scores: np.ndarray, lexical_scores: np.ndarray) -> np.ndarray:
    dense = min_max(dense_scores)
    lexical = min_max(lexical_scores)
    return (0.85 * dense) + (0.15 * lexical)


def min_max(scores: np.ndarray) -> np.ndarray:
    if scores.size == 0:
        return scores
    minimum = float(np.min(scores))
    maximum = float(np.max(scores))
    if maximum <= minimum:
        return np.zeros_like(scores, dtype=np.float32)
    return ((scores - minimum) / (maximum - minimum)).astype(np.float32)


def tokenize_search_text(chunk: Dict[str, Any]) -> List[str]:
    parts = [
        str(chunk.get("source", "")),
        str(chunk.get("title", "")),
        str(chunk.get("section", "")),
        str(chunk.get("text", "")),
    ]
    return tokenize("\n".join(parts))


def tokenize(text: str) -> List[str]:
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    expanded = expanded.replace("_", " ").replace("-", " ").replace("/", " ")
    return [token.lower() for token in re.findall(r"[A-Za-zА-Яа-я0-9]+", expanded)]


def save_index(index_dir: Path, chunks: List[Chunk], vectors: np.ndarray, manifest: Dict[str, Any]) -> Dict[str, Any]:
    index_dir.mkdir(parents=True, exist_ok=True)
    vectors = l2_normalize(vectors.astype(np.float32))

    write_jsonl(index_dir / "chunks.jsonl", [chunk.to_json() for chunk in chunks])
    np.save(index_dir / "vectors.npy", vectors)

    backend = "numpy"
    try:
        import faiss  # type: ignore

        faiss_index = faiss.IndexFlatIP(vectors.shape[1])
        faiss_index.add(vectors)
        faiss.write_index(faiss_index, str(index_dir / "index.faiss"))
        backend = "faiss"
    except ImportError:
        pass

    final_manifest = dict(manifest)
    final_manifest.update(
        {
            "backend": backend,
            "chunk_count": len(chunks),
            "dimension": int(vectors.shape[1]) if vectors.size else 0,
            "files": {
                "chunks": "chunks.jsonl",
                "vectors": "vectors.npy",
                "faiss": "index.faiss" if backend == "faiss" else None,
            },
        }
    )
    write_json(index_dir / "manifest.json", final_manifest)
    return final_manifest


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")
