# CoTran — Project Context

## Current Status
Step 1 complete. Full pipeline working end-to-end on entire FastAPI repo. Runs in ~3.5 minutes. Moving to Step 2.

## Active Branch
feat/backend-pipeline

## Completed: Step 1 — Backend ingestion pipeline
Goal: Parse a local repo, chunk by function/class, embed with OpenAI, store in Pinecone, query returns relevant chunks

**Definition of Done — MET:**
Point ingest.py at the FastAPI repo, run it, Pinecone has meaningful chunks stored, test query returns top 3 relevant code chunks ✓

## Key Decisions Made
- Python only for parsing in Step 1, multi-language later
- Chunking strategy: function-level and class-level chunks
- Test repo: FastAPI (~10k-15k lines, Python only) — cloned at /Users/donghoon/Desktop/ct_home/fastapi
- Parser: tree-sitter + tree-sitter-python
- Embedding model: OpenAI text-embedding-3-small
- Vector DB: Pinecone (free tier, us-east-1, serverless)
- Pinecone index name: cotran-v1
- Batch size: 50 vectors per upsert call
- Chunk truncation: 4000 chars for metadata, 8000 chars for embeddings

## What's Working
- `walk_repo(repo)` — walks a directory, returns list of all `.py` file paths
- `walk_node(node, chunks)` — recursively traverses AST, collects function/class nodes
- `parse_chunks(filepath)` — parses a .py file with tree-sitter, returns list of chunk bytes
- `get_openai_embeddings(chunks)` — batches all chunks per file, one OpenAI call per file
- `upsert_to_pinecone(chunks, vectors)` — batches upserts in groups of 50
- `test_query(query)` — embeds query, searches Pinecone, returns top 3 matches
- Full pipeline runs on entire FastAPI repo in ~3.5 minutes

## File Structure
cotran/
  README.md
  CONTEXT.md
  step1-plan.md
  ingest.py

## Known Limitations (future steps)
- Ingestion speed: ~3.5 min, target <2 min — fix with async API calls
- Chunk IDs are not stable across runs (chunk-0, chunk-1...) — duplicates on re-run
- No error recovery if pipeline fails mid-run

## Next Session Start Point
Start Step 2 — build main.py with the /orient endpoint. Takes a fixed request, searches Pinecone, sends chunks to Claude Sonnet 4.6, returns a structured orientation document.
