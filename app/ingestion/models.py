"""Data shapes shared by the ingestion pipeline."""
from dataclasses import dataclass, field


@dataclass
class Section:
    """A piece of a document as it came out of the parser, before chunking."""
    text: str
    page: int | None = None      # 1-based page number (PDFs only)
    heading: str | None = None   # nearest heading above this text


@dataclass
class Document:
    doc_id: str
    source: str                  # file name, shown in citations
    sections: list[Section]
    allowed_roles: list[str] = field(default_factory=lambda: ["all"])


@dataclass
class Chunk:
    """The unit we embed, search and cite."""
    chunk_id: str
    doc_id: str
    source: str
    text: str
    page: int | None
    heading: str | None
    allowed_roles: list[str]

    def citation(self) -> str:
        parts = [self.source]
        if self.page:
            parts.append(f"p.{self.page}")
        if self.heading:
            parts.append(f"§ {self.heading}")
        return ", ".join(parts)
