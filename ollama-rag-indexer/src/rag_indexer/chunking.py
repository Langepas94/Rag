import hashlib
import re
from typing import Iterable, List, Sequence, Tuple

from .models import Chunk, Document


Section = Tuple[str, str, int, int]


def fixed_chunk_documents(
    documents: Sequence[Document],
    max_chars: int = 1200,
    overlap: int = 180,
    strategy: str = "fixed",
) -> List[Chunk]:
    chunks: List[Chunk] = []
    for document in documents:
        sections = section_positions(document)
        for text, start, end in split_window(document.text, max_chars, overlap):
            section = section_at(sections, start) or document.section or document.title
            chunks.append(
                make_chunk(
                    document=document,
                    strategy=strategy,
                    index=len(chunks),
                    section=section,
                    text=text,
                    start_char=start,
                    end_char=end,
                )
            )
    return chunks


def structural_chunk_documents(
    documents: Sequence[Document],
    max_chars: int = 1800,
    overlap: int = 160,
) -> List[Chunk]:
    chunks: List[Chunk] = []
    for document in documents:
        for section, text, start, end in structural_sections(document):
            if len(text) <= max_chars:
                chunks.append(
                    make_chunk(
                        document=document,
                        strategy="structural",
                        index=len(chunks),
                        section=section,
                        text=text,
                        start_char=start,
                        end_char=end,
                    )
                )
                continue

            for part, local_start, local_end in split_window(text, max_chars, overlap):
                chunks.append(
                    make_chunk(
                        document=document,
                        strategy="structural",
                        index=len(chunks),
                        section=section,
                        text=part,
                        start_char=start + local_start,
                        end_char=start + local_end,
                    )
                )
    return chunks


def structural_sections(document: Document) -> List[Section]:
    if document.kind == "markdown":
        return markdown_sections(document)
    if document.kind == "code":
        return code_sections(document)
    if document.kind == "pdf":
        return [(document.section or "page %s" % document.page, document.text, 0, len(document.text))]
    return text_sections(document)


def markdown_sections(document: Document) -> List[Section]:
    matches = list(re.finditer(r"^(#{1,6})\s+(.+)$", document.text, flags=re.MULTILINE))
    if not matches:
        return [(document.section or document.title, document.text, 0, len(document.text))]

    sections: List[Section] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document.text)
        body = document.text[match.end() : end].strip()
        if not body:
            continue
        heading = match.group(2).strip()
        sections.append((heading, document.text[start:end].strip(), start, end))
    return sections or [(document.section or document.title, document.text, 0, len(document.text))]


def text_sections(document: Document) -> List[Section]:
    matches = list(
        re.finditer(
            r"^(?:Section|Chapter|Part|Step)\s+\d+[:.\- ]+(.+)$",
            document.text,
            flags=re.MULTILINE | re.IGNORECASE,
        )
    )
    if not matches:
        return [(document.section or document.title, document.text, 0, len(document.text))]

    sections: List[Section] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document.text)
        sections.append((match.group(0).strip(), document.text[start:end].strip(), start, end))
    return sections


def code_sections(document: Document) -> List[Section]:
    pattern = code_symbol_pattern(document.language)
    matches = [match for match in pattern.finditer(document.text) if len(match.group("indent")) == 0]
    if not matches:
        return [(document.section or document.title, document.text, 0, len(document.text))]

    sections: List[Section] = []
    prelude = document.text[: matches[0].start()].strip()
    if prelude:
        sections.append(("file prelude", prelude, 0, matches[0].start()))

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(document.text)
        kind, name = code_symbol_name(match)
        sections.append(("%s %s" % (kind, name), document.text[start:end].strip(), start, end))
    return sections


def code_symbol_pattern(language: str) -> re.Pattern:
    if language == "rust":
        return re.compile(
            r"^(?P<indent>[ \t]*)(?:"
            r"(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+(?P<rust_fn>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:pub(?:\([^)]*\))?\s+)?struct\s+(?P<rust_struct>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:pub(?:\([^)]*\))?\s+)?enum\s+(?P<rust_enum>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:pub(?:\([^)]*\))?\s+)?trait\s+(?P<rust_trait>[A-Za-z_][A-Za-z0-9_]*)|"
            r"impl(?:\s*<[^>]+>)?\s+(?P<rust_impl>[A-Za-z_][A-Za-z0-9_:<>]*)|"
            r"(?:pub(?:\([^)]*\))?\s+)?mod\s+(?P<rust_mod>[A-Za-z_][A-Za-z0-9_]*)"
            r")",
            flags=re.MULTILINE,
        )
    if language in {"typescript", "javascript"}:
        return re.compile(
            r"^(?P<indent>[ \t]*)(?:"
            r"(?:export\s+)?(?:async\s+)?function\s+(?P<ts_fn>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:export\s+)?(?:const|let|var)\s+(?P<ts_const>[A-Za-z_][A-Za-z0-9_]*)\s*=|"
            r"(?:export\s+)?class\s+(?P<ts_class>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:export\s+)?interface\s+(?P<ts_interface>[A-Za-z_][A-Za-z0-9_]*)|"
            r"(?:export\s+)?type\s+(?P<ts_type>[A-Za-z_][A-Za-z0-9_]*)\s*="
            r")",
            flags=re.MULTILINE,
        )
    return re.compile(
        r"^(?P<indent>[ \t]*)(?:(?:async\s+)?def\s+(?P<py_fn>[A-Za-z_][A-Za-z0-9_]*)|"
        r"class\s+(?P<py_class>[A-Za-z_][A-Za-z0-9_]*)|"
        r"function\s+(?P<js_fn>[A-Za-z_][A-Za-z0-9_]*)|"
        r"export\s+function\s+(?P<js_export>[A-Za-z_][A-Za-z0-9_]*)|"
        r"const\s+(?P<js_const>[A-Za-z_][A-Za-z0-9_]*)\s*=)",
        flags=re.MULTILINE,
    )


def code_symbol_name(match: re.Match) -> Tuple[str, str]:
    for key, value in match.groupdict().items():
        if key == "indent" or not value:
            continue
        if key.endswith("class"):
            return "class", value
        if key.endswith("struct"):
            return "struct", value
        if key.endswith("enum"):
            return "enum", value
        if key.endswith("trait"):
            return "trait", value
        if key.endswith("impl"):
            return "impl", value
        if key.endswith("mod"):
            return "module", value
        if key.endswith("interface"):
            return "interface", value
        if key.endswith("type"):
            return "type", value
        return "function", value
    return "section", "unknown"


def section_positions(document: Document) -> List[Tuple[int, str]]:
    if document.kind == "markdown":
        return [(match.start(), match.group(2).strip()) for match in re.finditer(r"^(#{1,6})\s+(.+)$", document.text, flags=re.MULTILINE)]
    if document.kind == "code":
        return [(start, section) for section, _text, start, _end in code_sections(document)]
    if document.section:
        return [(0, document.section)]
    return [(0, document.title)]


def section_at(sections: Sequence[Tuple[int, str]], offset: int) -> str:
    current = sections[0][1] if sections else ""
    for start, section in sections:
        if start > offset:
            break
        current = section
    return current


def split_window(text: str, max_chars: int, overlap: int) -> Iterable[Tuple[str, int, int]]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    clean_text = text.strip()
    if not clean_text:
        return

    base_offset = text.find(clean_text)
    start = 0
    while start < len(clean_text):
        target = min(len(clean_text), start + max_chars)
        end = choose_break(clean_text, start, target, max_chars)
        if end <= start:
            end = target
        chunk = clean_text[start:end].strip()
        if chunk:
            leading = len(clean_text[start:end]) - len(clean_text[start:end].lstrip())
            trailing_end = end - (len(clean_text[start:end]) - len(clean_text[start:end].rstrip()))
            yield chunk, base_offset + start + leading, base_offset + trailing_end
        if end >= len(clean_text):
            break
        start = max(0, end - overlap)


def choose_break(text: str, start: int, target: int, max_chars: int) -> int:
    if target >= len(text):
        return len(text)
    window = text[start:target]
    lower_bound = int(max_chars * 0.55)
    candidates = [window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"), window.rfind(" ")]
    best = max(candidates)
    if best >= lower_bound:
        if window[best : best + 2] == ". ":
            return start + best + 1
        return start + best
    return target


def make_chunk(
    document: Document,
    strategy: str,
    index: int,
    section: str,
    text: str,
    start_char: int,
    end_char: int,
) -> Chunk:
    return Chunk(
        chunk_id=make_chunk_id(strategy, document.source, index),
        strategy=strategy,
        source=document.source,
        title=document.title,
        section=section or document.section or document.title,
        text=text,
        chunk_index=index,
        start_char=start_char,
        end_char=end_char,
        page=document.page,
        kind=document.kind,
        language=document.language,
        metadata={"char_count": len(text), "token_estimate": estimate_tokens(text)},
    )


def make_chunk_id(strategy: str, source: str, index: int) -> str:
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:10]
    return "%s:%s:%05d" % (strategy, digest, index)


def estimate_tokens(text: str) -> int:
    return max(1, int(len(re.findall(r"\w+|[^\w\s]", text)) * 1.15))
