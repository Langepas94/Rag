from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Document:
    source: str
    title: str
    text: str
    kind: str
    section: Optional[str] = None
    page: Optional[int] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    strategy: str
    source: str
    title: str
    section: str
    text: str
    chunk_index: int
    start_char: int
    end_char: int
    page: Optional[int] = None
    kind: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

