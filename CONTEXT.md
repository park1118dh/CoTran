# CoTran — Project Context

## Current Status
Step 1 complete. Full pipeline working end-to-end. Moving to Step 2.

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

## What's Working
- `walk_repo(repo)` — walks a directory, returns list of all `.py` file paths
- `walk_node(node, chunks)` — recursively traverses AST, collects function/class nodes
- `parse_chunks(filepath)` — parses a .py file with tree-sitter, returns list of chunk bytes
- `get_openai_embeddings(chunks)` — embeds a list of chunks with text-embedding-3-small
- `upsert_to_pinecone(chunks, vectors)` — creates index if needed, stores chunks + vectors
- `test_query(query)` — embeds query, searches Pinecone, returns top 3 matches

## File Structure
cotran/
  README.md
  CONTEXT.md
  step1-plan.md
  ingest.py

## Next Session Start Point
Step 1 is done. Plan Step 2 — scale ingest.py to run on the entire FastAPI repo (not just one file), then decide what Step 2 looks like beyond that.
