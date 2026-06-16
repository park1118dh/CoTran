from fastapi import FastAPI
from pydantic import BaseModel
from ingest import test_query
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key = os.environ.get("ANTHROPIC_API_KEY"))

app = FastAPI()
class OrientRequest(BaseModel):
    repo_path: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/orient")
async def orient(request: OrientRequest):
    prompt = "explain how this codebase works"
    sys_prompt =  """You are going to act as a onboarder to someone new to this codebase. Explain the codebase not overly technically, just enough that the person onboarding knows what the level of the codebase is.
     What I want you to do is 1. exlpain the codebase (max 2-3 sentences): basically describing what it is and what it does in the big picture
     2. How it works, describe the mainflow, input t output, step by step.
     3. Key components: identify key pieces (variables, functions, classes, etc) that play an important role in the codebase as a whole - (the important pieces in the order they appear in the flow, not a flat list)
     4. Where to start - if you were going to read or modify this codebase what do you open first
     Note the dynamic should be like one of those in game video game interactive tutorials, where the user is guided on where to click and stuff to gain familiarity
     Dont make it take too long, but at the same time make sure the user has enough time to build that web in their head"""
    query_response = test_query(prompt)
    content = ""
    for match in query_response.matches:
        content += match.metadata['text']
    message = client.messages.create(max_tokens = 1024,
                                     messages = [{"role":"user", "content": "Here is relevant code from the codebase:\n\n" + content + "\n\nExplain how this codebase works."}],
                                     model = "claude-sonnet-4-6",
                                     system = sys_prompt)
    return message