from fastapi import FastAPI
from pydantic import BaseModel
from ingest import test_query
from anthropic import Anthropic
import os

client = Anthropic(api_key = os.environ.get("ANTHROPIC_API_KEY"))

app = FastAPI()
class OrientRequest(BaseModel):
    repo_path: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/orient")
async def orient(request: OrientRequest):
    prompt = "Explain how this codebase works"
    query_response = test_query(prompt)
    content = ""
    for match in query_response.matches:
        content += match.metadata['text']
    message = client.messages.create(max_tokens = 1024,
                                     messages = [{"role":"user", "content": "Here is relevant code from the codebase:\n\n" + content + "\n\nExplain how this codebase works."}],
                                     model = "claude-sonnet-4-6")
    return message