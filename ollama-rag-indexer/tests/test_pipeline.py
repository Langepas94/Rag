import json

from rag_indexer.embeddings import HashEmbedder
from rag_indexer.pipeline import build_index, compare_indexes


def test_build_index_and_compare_with_hash_embedder(tmp_path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "README.md").write_text(
        "# Local RAG\n\n## Chunk Metadata\n\nsource title section chunk_id metadata retrieval\n",
        encoding="utf-8",
    )
    queries = tmp_path / "queries.json"
    queries.write_text(
        json.dumps(
            {
                "queries": [
                    {
                        "query": "chunk_id source title section metadata",
                        "expected_source": "README.md",
                        "expected_section": "Chunk Metadata",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    out = tmp_path / "indexes"
    embedder = HashEmbedder()
    fixed_manifest = build_index(corpus, out, "fixed", embedder)
    structural_manifest = build_index(corpus, out, "structural", embedder)

    assert fixed_manifest["chunk_count"] >= 1
    assert structural_manifest["chunk_count"] >= 1
    assert (out / "fixed" / "chunks.jsonl").exists()
    assert (out / "structural" / "vectors.npy").exists()

    report = compare_indexes(out, ["fixed", "structural"], HashEmbedder(), queries)

    assert report["strategies"]["fixed"]["retrieval"]["source_hit_at_1"] == 1.0
    assert report["strategies"]["structural"]["retrieval"]["source_hit_at_1"] == 1.0

