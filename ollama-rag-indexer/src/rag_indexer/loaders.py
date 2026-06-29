import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from pypdf import PdfReader

from .models import Document


TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".rst"}
PDF_EXTENSIONS = {".pdf"}
CODE_EXTENSIONS: Dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "shell",
    ".sql": "sql",
}
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "indexes",
    "reports",
}


def discover_files(root: Path) -> Iterable[Path]:
    root = root.resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        suffix = path.suffix.lower()
        if suffix in TEXT_EXTENSIONS or suffix in PDF_EXTENSIONS or suffix in CODE_EXTENSIONS:
            yield path


def load_documents(root: Path) -> List[Document]:
    root = root.resolve()
    documents: List[Document] = []
    for path in discover_files(root):
        relative = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        if suffix in PDF_EXTENSIONS:
            documents.extend(load_pdf(path, relative))
        elif suffix in CODE_EXTENSIONS:
            documents.append(load_code(path, relative, CODE_EXTENSIONS[suffix]))
        else:
            documents.append(load_text(path, relative))
    return [doc for doc in documents if doc.text.strip()]


def load_text(path: Path, source: str) -> Document:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return Document(
        source=source,
        title=extract_title(text, path.name),
        text=text,
        kind="markdown" if path.suffix.lower() in {".md", ".markdown"} else "text",
        section=None,
    )


def load_code(path: Path, source: str, language: str) -> Document:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return Document(
        source=source,
        title=path.name,
        text=text,
        kind="code",
        section=path.name,
        language=language,
    )


def load_pdf(path: Path, source: str) -> List[Document]:
    reader = PdfReader(str(path))
    title = path.stem
    docs: List[Document] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        docs.append(
            Document(
                source=source,
                title=title,
                text=text,
                kind="pdf",
                section="page %d" % index,
                page=index,
            )
        )
    return docs


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), None)
    return first_line[:80] if first_line else fallback


def estimate_page_count(documents: List[Document], chars_per_page: int = 3000) -> float:
    chars = sum(len(doc.text) for doc in documents)
    if chars_per_page <= 0:
        return 0.0
    return chars / float(chars_per_page)

