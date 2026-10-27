# DocSentinel — Permission-Aware Enterprise RAG with Verified Answers

Ask questions over company documents (PDF, DOCX, HTML, Markdown) and get answers that:
- **Respect access control**: users only see answers from documents they are allowed to read.
- **Cite their sources**: every claim links to the exact page and passage.
- **Check themselves**: a verifier scores each answer against the sources and refuses when evidence is weak.
- **Are measured**: an evaluation suite tracks retrieval and answer quality on every change.

## Architecture
```
Upload -> Parse (PDF/DOCX/HTML) -> Chunk (section-aware) -> Embed -> Vector DB (+ ACL metadata)
                                                              \-> BM25 keyword index
Question -> ACL filter -> Hybrid search (vector + BM25) -> Rerank -> LLM answer w/ citations
         -> Citation verifier -> Answer or "not enough evidence"
```

## Stack
Python 3.11+, FastAPI, Qdrant, sentence-transformers, rank-bm25, cross-encoder reranker,
pluggable LLM (Claude / OpenAI / Groq / local Ollama), Streamlit UI, Docker, pytest.

## Roadmap
1. Project setup ✅
2. Document ingestion (parsing + smart chunking) ✅
3. Embeddings + vector store
4. Hybrid search + reranking
5. Answer generation with citations
6. Permission-aware retrieval (RBAC)
7. Answer verification / hallucination guard
8. FastAPI backend
9. Chat UI
10. Evaluation suite
11. Docker + deployment + demo video

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt reportlab
python scripts/make_sample_docs.py     # demo docs for the fictional "Northwind Labs"
python scripts/ingest_preview.py       # see how documents are parsed and chunked
pytest -q
```
