# CoTran — Project Context

## Current Status
Step 3 in progress. Prompt engineering done, system prompt added, top_k increased to 20. Retrieval diversity is the remaining problem — same chunks keep coming back from the same corner of the repo.

## Active Branch
feat/backend-pipeline

## Completed: Step 1 — Backend ingestion pipeline ✓
## Completed: Step 2 — FastAPI backend with /orient endpoint ✓
## Step 3 — Prompt engineering and retrieval quality ✓

## Step 4 — LLM-powered query generation
### Done
- Changed 1 query prompt to 4 query prompts each getting top 5 queries for more diversity
- Output is no longer JSON, and comes out as text

### Remaining
- Implementing LLM powered querying

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
- top_k: 20

## File Structure
cotran/
  README.md
  CONTEXT.md
  step1-plan.md
  step2-plan.md
  ingest.py
  main.py
  .env (gitignored)

## Known Limitations
- Retrieval diversity: hardcoded queries are FastAPI-specific hacks, not general — need LLM-generated queries
- Chunk IDs not stable across runs — duplicates on re-run (current fix: delete + recreate index on each ingest)
- Ingestion speed ~3.5 min — fix with async later

## Next Session Start Point
Implement LLM-generated query generation in main.py:
1. Before querying Pinecone, walk the repo file tree and send it to Claude
2. Ask Claude to generate 4-5 targeted search queries specific to that codebase
3. Use those queries to search Pinecone instead of the current hardcoded prompts
Goal: retrieval that works on any repo, not just FastAPI
