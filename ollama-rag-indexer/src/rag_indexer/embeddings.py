import hashlib
import re
from typing import Iterable, List, Optional

import numpy as np
import requests


class Embedder:
    name = "base"
    dimension: Optional[int] = None

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        raise NotImplementedError


class OllamaEmbedder(Embedder):
    name = "ollama"

    def __init__(
        self,
        model: str = "qwen3-embedding",
        base_url: str = "http://localhost:11434",
        batch_size: int = 16,
        timeout: int = 180,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.batch_size = batch_size
        self.timeout = timeout
        self.dimension: Optional[int] = None

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        items = list(texts)
        if not items:
            return np.zeros((0, 0), dtype=np.float32)

        vectors: List[List[float]] = []
        for start in range(0, len(items), self.batch_size):
            batch = items[start : start + self.batch_size]
            try:
                response = requests.post(
                    "%s/api/embed" % self.base_url,
                    json={"model": self.model, "input": batch},
                    timeout=self.timeout,
                )
            except requests.RequestException as exc:
                raise RuntimeError(
                    "Could not reach Ollama at %s. Start Ollama and pull the embedding model '%s'."
                    % (self.base_url, self.model)
                ) from exc
            response.raise_for_status()
            payload = response.json()
            embeddings = payload.get("embeddings")
            if embeddings is None:
                single = payload.get("embedding")
                embeddings = [single] if single is not None else None
            if not embeddings:
                raise RuntimeError("Ollama response did not contain embeddings")
            if len(embeddings) != len(batch):
                raise RuntimeError("Ollama returned %d embeddings for %d inputs" % (len(embeddings), len(batch)))
            vectors.extend(embeddings)

        matrix = np.asarray(vectors, dtype=np.float32)
        self.dimension = int(matrix.shape[1])
        return l2_normalize(matrix)


class HashEmbedder(Embedder):
    name = "hash"

    def __init__(self, dimension: int = 384) -> None:
        self.dimension = dimension
        self.model = "hash-%d" % dimension

    def embed(self, texts: Iterable[str]) -> np.ndarray:
        items = list(texts)
        matrix = np.zeros((len(items), self.dimension), dtype=np.float32)
        for row, text in enumerate(items):
            for token in tokenize(text):
                digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
                number = int.from_bytes(digest, "big")
                column = number % self.dimension
                sign = 1.0 if (number >> 63) & 1 else -1.0
                matrix[row, column] += sign
        return l2_normalize(matrix)


def get_embedder(
    kind: str,
    model: Optional[str] = None,
    ollama_url: str = "http://localhost:11434",
    batch_size: int = 16,
    timeout: int = 180,
) -> Embedder:
    if kind == "ollama":
        return OllamaEmbedder(model=model or "qwen3-embedding", base_url=ollama_url, batch_size=batch_size, timeout=timeout)
    if kind == "hash":
        return HashEmbedder()
    raise ValueError("Unknown embedder: %s" % kind)


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_]+", text)]


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    if matrix.size == 0:
        return matrix.astype(np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return (matrix / norms).astype(np.float32)
