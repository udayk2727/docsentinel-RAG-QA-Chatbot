# DocSentinel: project notes for Claude Code

Permission-aware enterprise RAG Q&A chatbot built as a portfolio project.
We build it together **one step at a time**: after each step, explain in simple
language what was built and why, give a one-line "interview line", run the tests,
commit, then wait for the user to say "next".

## Stack
Python 3.11+, FastAPI, Qdrant, sentence-transformers (BAAI/bge-small-en-v1.5),
rank-bm25, cross-encoder reranker, Claude via the `anthropic` SDK (LLM_PROVIDER=anthropic),
Streamlit UI, Docker, pytest. Settings live in `app/config.py` (read from `.env`).

## Layout
- `app/ingestion/`: parsers (PDF/DOCX/HTML/MD) and sentence/section-aware chunker
- `app/retrieval/`: embeddings, vector store, BM25, hybrid search, reranking
- `app/generation/`: Claude answers with citations
- `app/security/`: role-based access filters
- `app/api/`: FastAPI backend
- `ui/`: chat UI; `eval/`: evaluation suite; `tests/`: pytest
- `data/sample_docs/`: demo docs for fictional "Northwind Labs"; `acl.json` maps file -> allowed roles

## Roadmap
1. Project setup ✅
2. Document ingestion ✅
3. Embeddings + vector store (Qdrant) <- NEXT
4. Hybrid search (vector + BM25) + cross-encoder reranking
5. Answer generation with citations (Claude)
6. Permission-aware retrieval (filter by user role inside the vector search)
7. Answer verification / hallucination guard (refuse when evidence is weak)
8. FastAPI backend
9. Chat UI (Streamlit) showing citations and role switcher
10. Evaluation suite (retrieval hit-rate, MRR, faithfulness) with reported numbers
11. Docker, deployment, README polish, demo video

## Commands
```bash
python scripts/make_sample_docs.py
python scripts/ingest_preview.py
pytest -q
```
