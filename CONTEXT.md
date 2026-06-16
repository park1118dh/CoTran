# CoTran — Project Context

## Current Status
Step 3 in progress. Prompt engineering done, system prompt added, top_k increased to 20. Retrieval diversity is the remaining problem — same chunks keep coming back from the same corner of the repo.

## Active Branch
feat/backend-pipeline

## Completed: Step 1 — Backend ingestion pipeline ✓
## Completed: Step 2 — FastAPI backend with /orient endpoint ✓

## Step 3 — Prompt engineering and retrieval quality
### Done
- System prompt added to Claude call (structured onboarding tone, 4 sections)
- top_k increased from 3 to 20
- chunk metadata now stores type (function_definition/class_definition) and length
- .env file set up — no more manual exports

### Remaining
- Retrieval diversity: all 20 chunks come from the same part of the repo
- Fix: send multiple targeted queries to Pinecone and deduplicate results
- Re-run ingest.py to populate Pinecone with new type/length metadata
- Return only Claude text, not full message object

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
- Retrieval diversity: chunks cluster around same repo section
- Chunk IDs not stable across runs — duplicates on re-run
- Ingestion speed ~3.5 min — fix with async later
- Claude response returned as full message object, not just text

## Next Session Start Point
1. Re-run ingest.py to repopulate Pinecone with type/length metadata
2. Replace single query with multiple targeted queries in main.py, deduplicate results
3. Return only message.content[0].text from /orient instead of full message object
