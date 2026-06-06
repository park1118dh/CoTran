Decisions and Planning of Step 2 (Sending the users request to the pipeline)

Problem this step solves: We have confirmed that the pipeline effectively parses and chunks code, and now need to add the feature of sending the user input to be processed in the pipeline. The first step is to be able to take a query from the user, and search for it in Pinecone for relevant chunks in order to send ot Claude.

Request: The final system planned takes and reads a codebase, and then the user asks it to generate an explanation. This is not an open ended request. This is mode 1, and the purpose is to give an explanation of the codebase, nothing else. So the user only has the option to compile an explanation, not any other open ended request.

Test Repo: FastAPI opensource repo. This is repo is approximately 10000-15000 lines of code. Not the biggest repo, but enough size to test whether the product will work with real existing repos, not only small toy repos. FastAPI is part of the tech stack, and is an essential tool that is used by many builders, including me. Finally, we are building V1 to operate on python only, and the FastAPI codebase is only python.

Claude model: CLaude Sonnet 4.6

Claude returns Orientation docmument:
- Purpose of the codebase in plain language
- Primary input — what goes in and where it enters
- Step-by-step flow through the system — which functions handle what,in    order
- Key components and what they do
- Entry points and how to start navigating
- Dependencies and why they exist

Files created: main.py

main.py: contains the /orient endpoint, that takes the query from the user and searches through the database.

Defintion of done: When we hit the /orient endpoint, we get a real orientation document. No panel yet.

