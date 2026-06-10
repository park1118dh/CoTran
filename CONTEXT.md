# CoTran — Project Context

## Current Status
Step 2 complete. /orient endpoint working end-to-end. Moving to Step 3 — prompt engineering and retrieval quality.

## Active Branch
feat/backend-pipeline

## Completed: Step 1 — Backend ingestion pipeline
Goal: Parse a local repo, chunk by function/class, embed with OpenAI, store in Pinecone, query returns relevant chunks ✓

## Completed: Step 2 — FastAPI backend with /orient endpoint
Goal: Hit /orient, get back a real orientation document from Claude ✓

**Definition of Done — MET:**
curl request to /orient returns a structured orientation document for the FastAPI repo ✓

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
- Claude model: claude-sonnet-4-6

## What's Working
- `walk_repo(repo)` — walks a directory, returns list of all `.py` file paths
- `walk_node(node, chunks)` — recursively traverses AST, collects function/class nodes
- `parse_chunks(filepath)` — parses a .py file with tree-sitter, returns list of chunk bytes
- `get_openai_embeddings(chunks)` — batches all chunks per file, one OpenAI call per file
- `upsert_to_pinecone(chunks, vectors)` — batches upserts in groups of 50
- `test_query(query)` — embeds query, searches Pinecone, returns top 3 matches
- `GET /` — health check
- `POST /orient` — receives repo_path, queries Pinecone, sends chunks to Claude, returns orientation document

## File Structure
cotran/
  README.md
  CONTEXT.md
  step1-plan.md
  step2-plan.md
  ingest.py
  main.py

## Known Limitations (next steps)
- Only retrieving top 3 chunks — not enough context for a full orientation document
- Prompt is generic — output not meaningfully different from "explain this repo" in Claude Code
- No structured output format enforced
- Chunk IDs not stable across runs — duplicates on re-run
- Ingestion speed ~3.5 min — fix with async later

## Next Session Start Point
Step 3 — improve retrieval (top 20-30 chunks) and prompt engineering (structured output format: purpose, flow, components in order). Goal: output that is meaningfully better than Claude Code.
