from pathlib import Path
from textwrap import fill


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EVALUATION = ROOT / "evaluation"
GENERATED_SOURCES = ROOT / "generated_sources"


TOPICS = [
    ("Ingestion Contract", "loaders preserve source paths, document titles, page numbers, and a stable kind field"),
    ("Chunk Metadata", "every chunk carries source, title, section, chunk_id, offsets, and page information when available"),
    ("Fixed Windows", "fixed chunking uses bounded character windows with overlap and whitespace-aware break points"),
    ("Structural Boundaries", "structural chunking starts from headings, pages, files, classes, and functions"),
    ("Embedding Backend", "Ollama embeddings are requested through the local HTTP API and stored as normalized vectors"),
    ("Vector Storage", "FAISS is used when installed and NumPy vectors remain available as a portable fallback"),
    ("Retrieval Metrics", "comparison uses hit at k, reciprocal rank, source accuracy, and section accuracy"),
    ("Operational Checks", "the pipeline verifies document count, estimated pages, chunk counts, and metadata coverage"),
]


def main() -> None:
    write_readme()
    write_article(
        CORPUS / "articles" / "retrieval_architecture.md",
        "Retrieval Architecture Notes",
        34,
        "architecture",
    )
    write_article(
        CORPUS / "articles" / "chunking_evaluation.md",
        "Chunking Evaluation Field Guide",
        32,
        "evaluation",
    )
    write_code()
    write_pdf_source()
    write_pdf()
    write_queries()
    print("Sample corpus written to %s" % CORPUS)


def write_readme() -> None:
    path = CORPUS / "README.md"
    body = ["# Local RAG Corpus", ""]
    for number, (title, detail) in enumerate(TOPICS, start=1):
        body.append("## %s" % title)
        body.append("")
        body.append(paragraph(number, title, detail, "readme"))
        body.append("")
    write_text(path, "\n".join(body))


def write_article(path: Path, title: str, sections: int, label: str) -> None:
    body = ["# %s" % title, ""]
    for number in range(1, sections + 1):
        topic, detail = TOPICS[(number - 1) % len(TOPICS)]
        body.append("## Section %02d: %s" % (number, topic))
        body.append("")
        body.append(paragraph(number, topic, detail, label))
        body.append("")
        body.append(paragraph(number + sections, topic, detail, "%s-deep-dive" % label))
        body.append("")
    write_text(path, "\n".join(body))


def paragraph(number: int, title: str, detail: str, label: str) -> str:
    sentences = [
        "This %s note describes %s." % (label, detail),
        "The section is intentionally verbose so that indexing tests have enough material to form realistic chunks.",
        "A retrieval system should keep the relationship between the user question, the original source, and the surrounding section visible.",
        "When a chunk crosses a boundary, the answer may still be relevant, but the metadata becomes less precise for review and citation.",
        "When a chunk is too small, it can lose setup, definitions, and examples that make the result useful to a reader.",
        "The preferred implementation records offsets, stable identifiers, and plain text so that a later answer can cite the exact file or page.",
        "Topic marker %03d repeats the phrase %s to make evaluation queries deterministic without hiding the normal prose around it."
        % (number, title.lower()),
    ]
    return fill(" ".join(sentences), width=88)


def write_code() -> None:
    path = CORPUS / "code" / "sample_indexing_service.py"
    lines = [
        '"""Reference service used as code material for chunking tests."""',
        "",
        "from dataclasses import dataclass",
        "from typing import Dict, Iterable, List",
        "",
        "",
        "@dataclass",
        "class ChunkRecord:",
        "    chunk_id: str",
        "    source: str",
        "    title: str",
        "    section: str",
        "    text: str",
        "    metadata: Dict[str, str]",
        "",
        "",
    ]
    for number in range(1, 24):
        lines.extend(
            [
                "def build_stage_%02d(records: Iterable[ChunkRecord]) -> List[ChunkRecord]:" % number,
                '    """Apply indexing stage %02d with metadata validation and retrieval notes."""' % number,
                "    output: List[ChunkRecord] = []",
                "    for record in records:",
                "        metadata = dict(record.metadata)",
                '        metadata["stage"] = "stage_%02d"' % number,
                '        metadata["quality_note"] = "preserve source title section chunk_id for retrieval"',
                "        output.append(",
                "            ChunkRecord(",
                "                chunk_id=record.chunk_id,",
                "                source=record.source,",
                "                title=record.title,",
                "                section=record.section,",
                "                text=record.text,",
                "                metadata=metadata,",
                "            )",
                "        )",
                "    return output",
                "",
                "",
            ]
        )
    write_text(path, "\n".join(lines))


def write_pdf_source() -> None:
    path = GENERATED_SOURCES / "pdf_sources" / "operations_playbook.txt"
    lines = ["Operations Playbook for Local RAG Indexes", ""]
    for number in range(1, 30):
        topic, detail = TOPICS[(number - 1) % len(TOPICS)]
        lines.append("Chapter %02d - %s" % (number, topic))
        lines.append("")
        lines.append(paragraph(number, topic, detail, "pdf-playbook"))
        lines.append("")
        lines.append(paragraph(number + 100, topic, detail, "pdf-playbook"))
        lines.append("")
    write_text(path, "\n".join(lines))


def write_pdf() -> None:
    source = GENERATED_SOURCES / "pdf_sources" / "operations_playbook.txt"
    target = CORPUS / "papers" / "operations_playbook.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.pdfgen import canvas
    except ImportError:
        print("reportlab is not installed; skipping PDF generation")
        return

    text = source.read_text(encoding="utf-8")
    pdf = canvas.Canvas(str(target), pagesize=LETTER)
    width, height = LETTER
    x = 54
    y = height - 54
    line_height = 13
    pdf.setFont("Times-Roman", 10)
    for raw_line in text.splitlines():
        wrapped = [raw_line] if not raw_line else wrap_line(raw_line, width=92)
        for line in wrapped:
            if y < 54:
                pdf.showPage()
                pdf.setFont("Times-Roman", 10)
                y = height - 54
            pdf.drawString(x, y, line)
            y -= line_height
    pdf.save()


def write_queries() -> None:
    queries = {
        "queries": [
            {
                "query": "How are source title section and chunk_id stored for every chunk?",
                "expected_source": "README.md",
                "expected_section": "Chunk Metadata",
            },
            {
                "query": "Which strategy uses bounded character windows with overlap?",
                "expected_source": "README.md",
                "expected_section": "Fixed Windows",
            },
            {
                "query": "What boundaries does structural chunking use before fallback splitting?",
                "expected_source": "README.md",
                "expected_section": "Structural Boundaries",
            },
            {
                "query": "Where are hit at k reciprocal rank and section accuracy described?",
                "expected_source": "articles/chunking_evaluation.md",
                "expected_section": "Retrieval Metrics",
            },
            {
                "query": "Which notes describe FAISS and NumPy vectors as storage backends?",
                "expected_source": "articles/retrieval_architecture.md",
                "expected_section": "Vector Storage",
            },
            {
                "query": "What code function applies indexing stage 12 with metadata validation?",
                "expected_source": "code/sample_indexing_service.py",
                "expected_section": "function build_stage_12",
            },
            {
                "query": "Which PDF chapter explains operational checks for document count and metadata coverage?",
                "expected_source": "papers/operations_playbook.pdf",
                "expected_section": "page",
            },
            {
                "query": "How does the embedding backend request local vectors from Ollama?",
                "expected_source": "articles/retrieval_architecture.md",
                "expected_section": "Embedding Backend",
            },
            {
                "query": "Why can chunks that are too small lose setup definitions and examples?",
                "expected_source": "articles/chunking_evaluation.md",
                "expected_section": "Chunk Metadata",
            },
            {
                "query": "What service record keeps source title section and metadata fields?",
                "expected_source": "code/sample_indexing_service.py",
                "expected_section": "class ChunkRecord",
            },
        ]
    }
    path = EVALUATION / "queries.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    import json

    path.write_text(json.dumps(queries, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def wrap_line(line: str, width: int) -> list:
    if len(line) <= width:
        return [line]
    words = line.split()
    lines = []
    current = []
    current_len = 0
    for word in words:
        if current and current_len + len(word) + 1 > width:
            lines.append(" ".join(current))
            current = [word]
            current_len = len(word)
        else:
            current.append(word)
            current_len += len(word) + 1
    if current:
        lines.append(" ".join(current))
    return lines


if __name__ == "__main__":
    main()
