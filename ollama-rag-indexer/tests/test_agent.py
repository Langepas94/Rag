from rag_indexer.agent import RagAgent, build_rag_user_message, evaluate_answer_pair
from rag_indexer.embeddings import HashEmbedder
from rag_indexer.pipeline import build_index
from rag_indexer.vector_store import SearchResult, VectorIndex


class RecordingChatClient:
    def __init__(self) -> None:
        self.messages = []

    def complete(self, messages):
        self.messages.append(messages)
        text = messages[-1]["content"]
        if "Retrieved context" in text:
            return "RAG answer cites tg-agent/README.md and mentions /connect HTTP stdio mcp_connect."
        return "Plain answer without project-specific sources."


def test_rag_agent_has_plain_and_rag_modes(tmp_path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "README.md").write_text(
        "# tg-agent\n\nRuntime MCP management uses /connect HTTP stdio and mcp_connect.\n",
        encoding="utf-8",
    )
    out = tmp_path / "indexes"
    embedder = HashEmbedder()
    build_index(corpus, out, "structural", embedder)

    chat = RecordingChatClient()
    agent = RagAgent(chat, HashEmbedder(), VectorIndex(out / "structural"), top_k=1)

    plain = agent.answer("How does the bot connect MCP servers?", use_rag=False)
    rag = agent.answer("How does the bot connect MCP servers?", use_rag=True)

    assert plain.mode == "plain"
    assert plain.sources == []
    assert rag.mode == "rag"
    assert rag.sources[0]["source"] == "README.md"
    assert "Retrieved context" not in chat.messages[0][-1]["content"]
    assert "Retrieved context" in chat.messages[1][-1]["content"]


def test_build_rag_user_message_includes_ranked_sources() -> None:
    result = SearchResult(
        {
            "source": "tg-agent/README.md",
            "section": "Runtime MCP management",
            "chunk_id": "abc",
            "text": "Use /connect and mcp_connect.",
        },
        0.9,
    )

    message = build_rag_user_message("How connect?", [result])

    assert "User question:" in message
    assert "[1] source=tg-agent/README.md" in message
    assert "Use /connect and mcp_connect." in message


def test_build_rag_user_message_preserves_user_language_instruction() -> None:
    message = build_rag_user_message("Как работают MCP?", [])

    assert "User question:" in message
    assert "If the user question is in Russian, answer in Russian." in message
    assert "Найденный контекст" in message


def test_evaluate_answer_pair_compares_plain_and_rag() -> None:
    row = evaluate_answer_pair(
        {
            "query": "How connect?",
            "expectation": "Mention /connect and mcp_connect.",
            "expected_contains": ["/connect", "mcp_connect"],
            "expected_sources": ["tg-agent/README.md"],
        },
        {
            "plain": {
                "answer": "Use a command.",
                "sources": [],
            },
            "rag": {
                "answer": "Use /connect and mcp_connect.",
                "sources": [{"source": "tg-agent/README.md"}],
            },
        },
    )

    assert row["plain"]["expectation_coverage"] == 0.0
    assert row["rag"]["expectation_coverage"] == 1.0
    assert row["rag"]["source_hit_at_5"] == 1
