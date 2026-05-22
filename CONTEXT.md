# CoTran — Project Context

## Current Status
Pre-Step 1. Repo initialized. README uploaded. Backend pipeline not started.

## Active Branch
feat/backend-pipeline

## Current Step
Step 1 — Backend ingestion pipeline
Building: ingest.py
Goal: Parse a local repo, chunk by function/class, embed with OpenAI, store in ChromaDB, query returns relevant chunks

## Definition of Done for Step 1
Point ingest.py at a real cloned repo, run it, ChromaDB has meaningful chunks stored, query returns relevant code chunks back

## Key Decisions Made
- Python only for parsing in Step 1, multi-language later
- Chunking strategy: TBD — deciding before writing code
- Test repo: TBD — picking before writing code

## What's Working
Nothing yet

## File Structure
cotran/
  README.md
  CONTEXT.md

## Next Session Start Point
Answer three questions then write ingest.py:
1. File types to parse
2. Chunking strategy
3. Test repo to use