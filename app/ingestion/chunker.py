"""Split sections into overlapping, sentence-aligned chunks.

Why not just cut every N characters?
- Cutting mid-sentence gives the embedding model half a thought, so search gets worse.
- Mixing two sections in one chunk blurs the topic and breaks citations.
So we: (1) never cross a section/page boundary, (2) break on sentence ends,
(3) carry a little overlap so facts on a boundary appear whole in at least one chunk,
(4) prefix the heading so a chunk like "It is 20 days." still says what "it" is.
"""
import re

from app.config import settings
from app.ingestion.models import Chunk, Document

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n{2,}")


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_END.split(text) if s and s.strip()]


def _pack(sentences: list[str], size: int, overlap: int) -> list[str]:
    chunks, current = [], []
    for sentence in sentences:
        # A single giant "sentence" (e.g. a table row dump) is hard-split.
        while len(sentence) > size:
            chunks.append(sentence[:size])
            sentence = sentence[size - overlap:]
        if current and len(" ".join(current + [sentence])) > size:
            chunks.append(" ".join(current))
            # Keep trailing sentences up to `overlap` characters as the next chunk's start.
            tail, length = [], 0
            for s in reversed(current):
                if length + len(s) > overlap:
                    break
                tail.insert(0, s)
                length += len(s) + 1
            current = tail
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def chunk_document(
    doc: Document,
    size: int = settings.chunk_size,
    overlap: int = settings.chunk_overlap,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for section in doc.sections:
        for piece in _pack(split_sentences(section.text), size, overlap):
            text = f"{section.heading}\n{piece}" if section.heading else piece
            chunks.append(Chunk(
                chunk_id=f"{doc.doc_id}-{len(chunks):04d}",
                doc_id=doc.doc_id,
                source=doc.source,
                text=text,
                page=section.page,
                heading=section.heading,
                allowed_roles=doc.allowed_roles,
            ))
    return chunks
