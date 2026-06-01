# CoTran — Project Context

## Current Status
Step 1 in progress. `walk_repo` and `parse_chunks` complete. Next: `embed_chunks`.

## Active Branch
feat/backend-pipeline

## Current Step
Step 1 — Backend ingestion pipeline
Building: ingest.py
Goal: Parse a local repo, chunk by function/class, embed with OpenAI, store in Pinecone, query returns relevant chunks

## Definition of Done for Step 1
Point ingest.py at the FastAPI repo, run it, Pinecone has meaningful chunks stored, test query returns top 3 relevant code chunks

## Key Decisions Made
- Python only for parsing in Step 1, multi-language later
- Chunking strategy: function-level and class-level chunks
- Test repo: FastAPI (~10k-15k lines, Python only) — cloned at /Users/donghoon/Desktop/ct_home/fastapi
- Parser: tree-sitter + tree-sitter-python
- Embedding model: OpenAI text-embedding-3-small
- Vector DB: Pinecone

## What's Working
- `walk_repo(repo)` — walks a directory, returns list of all `.py` file paths
- `parse_chunks(filepath)` — parses a .py file with tree-sitter, returns list of function/class text chunks as bytes

## File Structure
cotran/
  README.md
  CONTEXT.md
  step1-plan.md
  ingest.py

## Next Session Start Point
Write draft of `embed_chunks(chunks)` — takes list of chunk bytes, calls OpenAI text-embedding-3-small, returns list of vectors
