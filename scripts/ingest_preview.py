"""Parse and chunk every sample document and print what came out."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.ingestion.chunker import chunk_document
from app.ingestion.parsers import load_document

DOCS = Path(__file__).resolve().parent.parent / "data" / "sample_docs"
acl = json.loads((DOCS / "acl.json").read_text())

total = 0
for name, roles in acl.items():
    chunks = chunk_document(load_document(DOCS / name, roles))
    total += len(chunks)
    print(f"\n=== {name}  roles={roles}  chunks={len(chunks)}")
    for ch in chunks[:2]:
        print(f"  [{ch.citation()}] {ch.text[:90].replace(chr(10), ' | ')}...")
print(f"\nTotal chunks: {total}")
