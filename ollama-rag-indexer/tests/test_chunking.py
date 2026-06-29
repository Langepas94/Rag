from rag_indexer.chunking import fixed_chunk_documents, structural_chunk_documents
from rag_indexer.models import Document


def test_fixed_chunking_adds_required_metadata() -> None:
    doc = Document(
        source="README.md",
        title="Readme",
        kind="markdown",
        text="# Install\n\nRun the installer. " * 80,
    )

    chunks = fixed_chunk_documents([doc], max_chars=180, overlap=30)

    assert len(chunks) > 1
    assert chunks[0].source == "README.md"
    assert chunks[0].title == "Readme"
    assert chunks[0].section == "Install"
    assert chunks[0].chunk_id.startswith("fixed:")
    assert chunks[0].metadata["char_count"] == len(chunks[0].text)


def test_structural_chunking_keeps_markdown_sections() -> None:
    doc = Document(
        source="guide.md",
        title="Guide",
        kind="markdown",
        text="# Guide\n\nIntro\n\n## Retrieval Metrics\n\nUse hit at k and MRR.\n\n## Storage\n\nUse FAISS.",
    )

    chunks = structural_chunk_documents([doc], max_chars=300, overlap=20)
    sections = [chunk.section for chunk in chunks]

    assert "Guide" in sections
    assert "Retrieval Metrics" in sections
    assert "Storage" in sections


def test_structural_chunking_finds_top_level_code_symbols() -> None:
    doc = Document(
        source="service.py",
        title="service.py",
        kind="code",
        language="python",
        text="class Store:\n    pass\n\n\ndef build_index():\n    return True\n",
    )

    chunks = structural_chunk_documents([doc], max_chars=300, overlap=20)
    sections = [chunk.section for chunk in chunks]

    assert "class Store" in sections
    assert "function build_index" in sections

