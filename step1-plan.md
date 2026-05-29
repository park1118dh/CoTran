Decisions and Planning of Step 1 (Prove the Pipeline Works)

Problem this step solves: Before scaling to be a flexible tool that works with various languages and repos, we will need to confrim that implementation can successfully carry out the purposes on CoTran in one language and one repo. The first step in doing so would be to make sure we can effectively parse and chunk code effectively for future implementation.

Parser — tree-sitter Parses code into an AST. Understands code structure the way a compiler does. Supports 40+ languages. Same foundation VS Code uses internally.
Embedding Model — OpenAI text-embedding-3-small Simple, fast, cheap. Gets V1 working. Swap for CodeBERT or Voyage code-3 later once eval framework can measure whether it actually improves retrieval.
Vector Database — Pinecone Managed, scales easily, free tier covers V1 entirely. ChromaDB ruled out for limited querying at scale. FAISS and Weaviate ruled out as overkill for V1.

Chunking Strategy: Chunk both in the class and function level. Chunking at the class level allows for understanding of broader scope of the repo, and gaining familiarity between how different components of code work together. Chunking at the function level is for building deep understanding of the codebase; understanding in depth how everything flows and what small roles allow for the repo to work.

Test Repo: FastAPI opensource repo. This is repo is approximately 10000-15000 lines of code. Not the biggest repo, but enough size to test whether the product will work with real existing repos, not only small toy repos. FastAPI is part of the tech stack, and is an essential tool that is used by many builders, including me. Finally, we are building V1 to operate on python only, and the FastAPI codebase is only python.

Files created: ingest.py

ingest.py: will take a local repo and turn it into a searchable vector database
