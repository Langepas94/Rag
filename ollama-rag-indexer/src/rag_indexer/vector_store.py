import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from .embeddings import l2_normalize
from .models import Chunk


class SearchResult:
    def __init__(self, chunk: Dict[str, Any], score: float) -> None:
        self.chunk = chunk
        self.score = score


class VectorIndex:
    def __init__(self, index_dir: Path) -> None:
        self.index_dir = Path(index_dir)
        self.manifest = read_json(self.index_dir / "manifest.json")
        self.chunks = read_jsonl(self.index_dir / "chunks.jsonl")
        self.vectors = np.load(self.index_dir / "vectors.npy").astype(np.float32)
        self.faiss_index = self._load_faiss()

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[SearchResult]:
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        query_vector = l2_normalize(query_vector.astype(np.float32))
        top_k = min(top_k, len(self.chunks))

        if self.faiss_index is not None:
            scores, indices = self.faiss_index.search(query_vector, top_k)
            return [
                SearchResult(self.chunks[int(index)], float(score))
                for score, index in zip(scores[0], indices[0])
                if int(index) >= 0
            ]

        scores = np.dot(self.vectors, query_vector[0])
        indices = np.argsort(-scores)[:top_k]
        return [SearchResult(self.chunks[int(index)], float(scores[int(index)])) for index in indices]

    def _load_faiss(self) -> Optional[Any]:
        faiss_path = self.index_dir / "index.faiss"
        if not faiss_path.exists():
            return None
        try:
            import faiss  # type: ignore
        except ImportError:
            return None
        return faiss.read_index(str(faiss_path))


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

