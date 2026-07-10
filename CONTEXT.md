# CoTran — Project Context

## Current Status
Backend MVP complete. /orient returns structured JSON with intro card and waypoints array. Ready for frontend (VS Code extension) development.

## Active Branch
feat/backend-pipeline

## Completed: Step 1 — Backend ingestion pipeline ✓
## Completed: Step 2 — FastAPI backend with /orient endpoint ✓
## Completed: Step 3 — Prompt engineering and retrieval quality ✓
## Completed: Step 4 — LLM-powered query generation ✓

### Step 4 Summary
- Claude receives the repo file tree (file paths only, not code)
- Generates 20 search queries based on those paths
- Queries run against Pinecone (top_k=5 each), results deduplicated
- Chunks fed to Claude with sys_prompt to produce the onboarding explanation
- sys_prompt tuned to output plain text, no markdown

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

## Mode 1 Direction (Updated)
Originally scoped as a panel that displays a prose orientation document. After further consideration, this was dropped — abstract text describing a codebase still leaves the user having to manually connect what they read to the actual code. That gap is where familiarity breaks down.

Mode 1 is now an interactive guided tour, inspired by game tutorials. The insight: a game tutorial doesn't describe the game to you, it puts you inside it and walks you through it. CoTran does the same — the user is always looking at real code, not a description of it.

How it works:
- Claude generates a sequence of 6-8 waypoints representing the spine of the codebase (entry point → core flow → key components)
- Each waypoint opens a specific file, highlights a specific line or range, and shows a short explanation
- The user can only advance by completing the action (go to this file, find this line) — not by just reading
- Tour length stays constant regardless of repo size; zoom level adjusts (function-level for small repos, module-level for large ones)
- At the end of the tour, the user has enough familiarity to start navigating and exploring on their own

Architecture shift:
- Backend output changes from prose to structured JSON (list of waypoints with file path, line range, explanation)
- Validation layer confirms file paths and line numbers exist before sending to extension
- Frontend is no longer a static panel — it drives file navigation, line highlighting, and callout UI inside VS Code

## Completed: Step 5 — Backend MVP ✓
- /orient returns structured JSON: {"intro": {"text": "..."}, "waypoints": [...]}
- Each waypoint has: filepath, line, description
- intro generated after waypoints so it can reference the exact concepts the tour uses
- Retrieval filters exclude test/, docs/, docs_src/, examples/, benchmarks/, scripts/, build/, dist/
- README fed into query generation (message1) to ground queries in actual codebase purpose
- sys_prompt tuned: plain language explanations, core files only, use exact line/path from metadata
- sys_prompt2 (intro): car dealership analogy, plain language, coherent with waypoints
- json.loads used to parse both outputs; strip_json_block helper handles markdown wrapper edge case

## Known Limitations
- Line numbers still occasionally guessed when Claude falls back to parametric knowledge (retrieval miss)
- Chunk IDs not stable across runs (current fix: delete + recreate index on each ingest)
- Ingestion speed ~3 min — fix with async later
- No validation layer yet — file paths not confirmed to exist before returning

## Completed: Step 6 — VS Code Extension Scaffold + Intro Card ✓
- Scaffolded VS Code extension with TypeScript (yo code)
- Extension activates, POSTs to /orient with workspace folder path
- Receives {intro, waypoints} JSON from backend
- Displays intro card text in a webview panel
- Loading message shown while backend processes
- Command registered as 'cotran.helloWorld' (rename to 'cotran.startTour' next)

## Completed: Step 7 — Webview panel with Start Tour button ✓
- Panel shows intro text and "Start Tour" button
- Button sends postMessage to extension with {command: 'next', index: 0}
- Extension listens with onDidReceiveMessage, opens the file at waypoint.filepath
- Uses vscode.workspace.openTextDocument + vscode.window.showTextDocument

## Next Session Start Point
Three things to add in order:
1. Jump to the correct line — add {selection: new vscode.Range(line, 0, line, 0)} to showTextDocument
   - waypoint.line is the line number, vscode.Range is 0-indexed so subtract 1
2. Highlight the line — use editor.setDecorations with a colored background decoration
   - vscode.window.createTextEditorDecorationType({backgroundColor: 'rgba(255,255,0,0.3)'})
3. Advance through waypoints — track current index, update panel HTML to show current waypoint explanation and "Next" button that sends the next index
   - When index >= waypoints.length, show "Tour complete" message
