from rag_indexer.embeddings import HashEmbedder
from rag_indexer.pipeline import build_index
from rag_indexer.retrieval import RetrievalSettings, filter_relevant, retrieve_with_settings, rewrite_search_query
from rag_indexer.vector_store import SearchResult, VectorIndex, tokenize


class FailingEmbedder:
    def embed(self, texts):
        raise AssertionError("lexical search must not call the embedder")


def test_rewrite_search_query_adds_project_aliases() -> None:
    rewritten = rewrite_search_query("How does the Telegram bot connect to MCP servers?")

    assert rewritten.startswith("How does the Telegram bot connect to MCP servers?")
    assert "tg-agent" in rewritten
    assert "mcp_client" in rewritten


def test_rewrite_search_query_adds_project_aliases_for_russian() -> None:
    rewritten = rewrite_search_query("Как работают mcp в телеграм боте изнутри?")

    assert rewritten.startswith("Как работают mcp в телеграм боте изнутри?")
    assert "tg-agent" in rewritten
    assert "mcp_client" in rewritten
    assert "stdio" in rewritten


def test_filter_relevant_applies_similarity_threshold() -> None:
    results = [
        SearchResult({"chunk_id": "good"}, 0.91),
        SearchResult({"chunk_id": "weak"}, 0.79),
    ]

    filtered = filter_relevant(results, 0.8)

    assert [result.chunk["chunk_id"] for result in filtered] == ["good"]


def test_tokenize_keeps_cyrillic_terms() -> None:
    assert tokenize("Телеграм бот и MCP") == ["телеграм", "бот", "и", "mcp"]


def test_lexical_search_does_not_call_embedder(tmp_path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "README.md").write_text(
        "# Telegram bot\n\nUse /rag compare to show plain and RAG answers side by side.\n",
        encoding="utf-8",
    )
    out = tmp_path / "indexes"
    build_index(corpus, out, "structural", HashEmbedder())

    results = retrieve_with_settings(
        VectorIndex(out / "structural"),
        FailingEmbedder(),
        "telegram rag compare",
        RetrievalSettings(top_k=1, search_mode="lexical"),
    )

    assert results[0].chunk["source"] == "README.md"
