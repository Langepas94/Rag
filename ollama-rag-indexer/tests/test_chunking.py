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


def test_structural_chunking_finds_rust_symbols() -> None:
    doc = Document(
        source="mcp_client.rs",
        title="mcp_client.rs",
        kind="code",
        language="rust",
        text="pub struct McpClient {}\n\nimpl McpClient {\n    pub async fn call_tool(&self) {}\n}\n\npub enum Transport { Http }\n",
    )

    chunks = structural_chunk_documents([doc], max_chars=300, overlap=20)
    sections = [chunk.section for chunk in chunks]

    assert "struct McpClient" in sections
    assert "impl McpClient" in sections
    assert "enum Transport" in sections


def test_structural_chunking_finds_typescript_symbols() -> None:
    doc = Document(
        source="tools/analyze.ts",
        title="analyze.ts",
        kind="code",
        language="typescript",
        text="export interface CityScore {}\n\nexport const compareWeatherCities = () => true;\n\nexport function registerAnalyzeTools() {}\n",
    )

    chunks = structural_chunk_documents([doc], max_chars=300, overlap=20)
    sections = [chunk.section for chunk in chunks]

    assert "interface CityScore" in sections
    assert "function compareWeatherCities" in sections
    assert "function registerAnalyzeTools" in sections
