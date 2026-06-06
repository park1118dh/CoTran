from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class OrientRequest(BaseModel):
    repo_path: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/orient")
async def orient(request: OrientRequest):
    return request.repo_path