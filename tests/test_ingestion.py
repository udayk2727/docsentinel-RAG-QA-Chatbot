from pathlib import Path

import pytest

from app.ingestion.chunker import _pack, chunk_document, split_sentences
from app.ingestion.models import Document, Section
from app.ingestion.parsers import load_document

DOCS = Path(__file__).resolve().parent.parent / "data" / "sample_docs"


def test_sentence_split():
    assert split_sentences("One. Two! Three?") == ["One.", "Two!", "Three?"]


def test_chunks_respect_size_and_overlap():
    sentences = [f"Sentence number {i} is here." for i in range(40)]
    chunks = _pack(sentences, size=200, overlap=60)
    assert all(len(c) <= 200 for c in chunks)
    # The last sentence of one chunk reappears at the start of the next.
    assert chunks[0].split(". ")[-1].rstrip(".") in chunks[1]


def test_chunk_never_mixes_sections():
    doc = Document("d1", "x.md", [Section("Alpha fact.", heading="A"), Section("Beta fact.", heading="B")])
    chunks = chunk_document(doc)
    assert [c.heading for c in chunks] == ["A", "B"]
    assert chunks[0].text.startswith("A\n")


@pytest.mark.parametrize("name", ["employee_handbook.md", "compensation_bands.docx",
                                  "incident_runbook.html", "security_policy.pdf"])
def test_every_format_parses(name):
    doc = load_document(DOCS / name)
    assert doc.sections and all(s.text for s in doc.sections)


def test_pdf_keeps_page_numbers():
    chunks = chunk_document(load_document(DOCS / "security_policy.pdf"))
    phishing = [c for c in chunks if "phishing" in c.text]
    assert phishing and phishing[0].page == 2


def test_same_file_same_id():
    assert load_document(DOCS / "employee_handbook.md").doc_id == load_document(DOCS / "employee_handbook.md").doc_id
