# Cotran
VS code extension that generates codebase orientation document to remove the translation barrier when opening unfamiliar repos.

CoTran — Codebase Translation Tool
Remove the roadblock between understanding a codebase and building with it.


The Problem
Every time you open an unfamiliar codebase — for an internship, open source contribution, or new project — there's a translation period that is grueling, tedious, and kills motivation before you even start building.

Current tools like Claude Code and Cursor exist, but they give you exact descriptions, not mental models. You get information without understanding. The result: you either fully offload to AI and lose ownership of your own code, or you quit.

There's a second problem that compounds this. Even once you understand a codebase, syntax friction slows you to a crawl. Every line becomes a lookup. Every function becomes a context switch. The path of least resistance becomes vibe-coding low quality output instead of building intentionally.

CoTran addresses both.


What CoTran Does
CoTran is a VS Code extension with a Python backend. It has three features across two modes.


Mode 1 — Codebase Orientation (Priority)
When you open a repository, CoTran generates a structured guided walkthrough of the codebase displayed as a VS Code panel.

Not a file-by-file dump. A narrative.

The orientation document contains:

Purpose of the codebase in plain language
Primary input — what goes in and where it enters
Step-by-step flow through the system — which functions handle what, in order
Key components and what they do
Entry points and how to start navigating
Dependencies and why they exist

The difference from Claude Code: Claude Code gives you exact descriptions when you ask. CoTran gives you a mental model first, unprompted, structured the way a senior engineer would explain it to you on your first day. The ordering is the product.

How it works technically:

User opens a repo in VS Code
Extension sends repo path to FastAPI backend
Backend parses and chunks code files by function, class, and module
Chunks are embedded using OpenAI text-embedding-3-small and stored in ChromaDB
Retrieval identifies the most structurally significant components
Claude API synthesizes a structured orientation document
Document is displayed in a VS Code webview panel


Mode 2 — Syntax Assistant (After Mode 1 is complete)
Two features that remove syntax friction during active development.

Feature 1 — Line Explainer Highlight any line of code, right click, select "Explain this." CoTran returns a plain language explanation of exactly what that line does in the context of the surrounding code. No copy-pasting into a separate chat. No context loss.

Feature 2 — Syntax Fixer Write what you mean — broken syntax, pseudocode, half-formed logic. Highlight it, right click, select "Fix syntax." CoTran returns working code that matches your intent. You write with intent, CoTran handles execution correctness.

Why this matters: People vibe-code low quality software not because they don't care but because intentional building feels impossibly slow when every line is a lookup. If you can write what you mean and fix execution instantly, you stay in the builder mindset. This feature exists because syntax friction has killed real projects — something that I have faced countless times.

HOWEVER, CoTran is not designed to generate application logic autonomously. It is designed for situations where the developer already knows the intended behavior, but translation into repository-consistent syntax is slowed by unfamiliar frameworks, languages, or codebase conventions. Otherwise, the developer should just ask claude code, cursor, etc.


Tech Stack
Frontend — VS Code Extension

TypeScript
VS Code Extension API
Webview panel for orientation display
Context menu commands for Mode 2 features
Communicates with backend via REST API

Backend — FastAPI

Python
FastAPI REST API
Code file parsing and chunking
OpenAI text-embedding-3-small for embeddings
ChromaDB vector database
Anthropic Claude API for orientation generation and syntax assistance
Deployed on Render or Railway


Architecture
User opens repo in VS Code

        ↓

VS Code Extension (TypeScript)

        ↓

POST /orient  →  FastAPI Backend (Python)

                        ↓

                 Parse + chunk code files

                        ↓

                 Embed chunks → ChromaDB

                        ↓

                 Retrieve key structural components

                        ↓

                 Claude API → structured orientation

                        ↓

                 Return document to extension

        ↓

Display in VS Code webview panel


Build Sequence
Phase 1 — Learn the platform (Week 1-2)

TypeScript fundamentals
VS Code Extension API basics
Build a minimal hello world extension

Phase 2 — Backend pipeline (Week 3-4)

FastAPI server running locally
Code file parsing and chunking strategy
Embedding pipeline working
ChromaDB storing and retrieving chunks
Claude generating orientation document from retrieved context
Definition of done: curl request to /orient returns a real orientation document for a test repo

Phase 3 — Extension + backend connected (Week 5-7)

Extension sends repo path to backend
Orientation document displayed in VS Code webview panel
Mode 1 working end to end
Definition of done: open a real open source repo in VS Code, CoTran panel opens with a structured walkthrough that is genuinely useful

Phase 4 — Evaluation framework (Week 7-8)

Build small eval set — does the orientation accurately represent the codebase
Measure whether Claude is using retrieved context vs parametric knowledge
Iterate on chunking strategy based on results
Definition of done: a number you can defend — "orientation accuracy improved from X to Y after restructuring chunking"

Phase 5 — Mode 2 (Week 9-10, only if Mode 1 is complete)

Line explainer context menu command
Syntax fixer context menu command
Definition of done: highlight a line, get a plain explanation; write pseudocode, get working syntax back

Phase 6 — Polish and publish (Week 10-11)

Extension published to VS Code marketplace
Backend deployed to live URL
README and demo recording
Definition of done: anyone can install CoTran from the VS Code marketplace and use it on any repo


Why This Project
Built for a specific moment: you find an open source repo you want to contribute to, you have an idea, and then you open the codebase and the translation period kills your momentum before you write a single line. You shouldn't be blocked from building what you want to build because of translation friction that has nothing to do with your knowledge or capability.

CoTran is built by someone who has experienced this repeatedly. The goal is not to replace understanding — deep knowledge still requires putting in the hours. The goal is to remove the roadblock that stops people from even beginning.


Current Status
Mode 1 in progress. Mode 2 designed, not started.

