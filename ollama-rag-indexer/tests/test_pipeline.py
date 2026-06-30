import json

from rag_indexer.embeddings import HashEmbedder
from rag_indexer.pipeline import build_index, compare_indexes, evaluate_query
from rag_indexer.vector_store import SearchResult


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


def test_evaluate_query_accepts_multiple_expected_sources() -> None:
    query = {
        "query": "How does the bot connect MCP servers?",
        "expected_sources": ["tg-agent/README.md", "tg-agent/src/mcp_client.rs"],
        "expected_sections": ["Runtime MCP", "function connect"],
    }
    results = [
        SearchResult({"source": "tg-agent/AGENTS.md", "section": "Context"}, 0.9),
        SearchResult({"source": "tg-agent/src/mcp_client.rs", "section": "function connect"}, 0.8),
    ]

    row = evaluate_query(query, results)

    assert row["source_rank"] == 2
    assert row["section_rank"] == 2
    assert row["source_hit_at_3"] == 1
