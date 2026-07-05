from fastapi import FastAPI
from pydantic import BaseModel
from ingest import test_query, walk_repo
from anthropic import Anthropic
import os
from dotenv import load_dotenv
import ast
import json

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
    query_prompt = """You are given a list of file paths and a readme to a codebase. The codebase details are in pinecone. Given the file paths and the readme, your job is to generate 20 search queries based on them.
     Our goal is to find the contents in pinecone that gives us the information to be able to explain and describe the codebase, and this is the basis in how you should create these 20 search queries.
     The readme is the reference of the queries you generate. You can use the readme to capture the essence of the codebase: allowing for but not limited to deciding which filepaths are useful for familiarization and overall capture of the
     foundation and base of the codebase or what type of queries would be useful to search for contents that allow for familiarization of the codebase in order to navigate and explore it.
     Note: For example, this is the analogy; in an fps game, the player in the tutorial needs to learn how to shoot, move, and access items etc. Not learn every item in the game or every map layout, but know how to explore the different features of the game with the
     familiarization from the tutorial. Learning specific items or map details is for them to learn but they cant do it without knowing how to shoot, run, jump, etc.. Same thing applies for the queries you generate. They should aim to give the base of the codebase to the user.
     Give the output as a python list of strings, but do not wrap it around as a mark down code block"""
    sys_prompt =  """You are going to act as an onboarder to a codebase. Basically your task is to familiarize the codebase with the user enough for them to explore and begin working on it themselves.
    THE APPROACH YOU WILL FOLLOW: the whole interaction should be like a game tutorial. In a game tutorial, the player enters and are given way points. Whether thats in their hotbar or certain locations in the 
    tutorial map they have to go to. Same thing here. The game becomes the codebase, and the player is the user. Based on the information you receive, identify the spine of the codebase. The base fundamentals and features
    that the user needs to approach, explore, and build on the codebase. Your output should be 4-8 waypoints/checkpoints that make up the fundamental base spine of the codebase. Thus your output should be a list of elements in JSON format.
    Each element in this output list is a way point, which has fields of file path, line number and your brief explanation of the waypoint.
    Some things to note in your descriptions and explanations
    1. Don't assume the user is going to understand a description when you explain a library just as is. A lof of the concepts are new so they initially need just a plain word description so they can grasp what it at actually is.
    2. Prioritize files that represent core implementation, and avoid files, such as examples/docs/benchmarks/test stuites etc, that may take up a big portion of the files but do not add any useful information of the core of the codebase.
    3. When we give you the content you are going to sumamarize, there is also a field in that content that is line number, use that number exactly, do not guess the line number.
    4. The first waypoint after the intro should be about the core datastructure/algorithm/aspect/component etc. of the codebase
    5. The Line field in the content is the exact line number of that chunk, use it verbatim, never invent a line number.
    6. The Path field in the content is the exact file path of that chunk, use it verbatim, never invent a file path.
    **DO NOT WRAP IN A MARKDOQN CODE BLOCK, RAW JSON ONLY**
     """

    sys_prompt2 = """You are going to write an intro for a codebase. The scenario is, the user encounters a new codebase, and normally they would have to explore themselves, search up documentation, and overcome the dauntingly slow process of understanding a codebase.
    It is almost like they are walking in a car dealership for a new car. So many cars, don't know where to look, don't know the purchase/rent process, what fees aren't being disclosed etc. It's too much information to handle and learn alnone. So what do the dealerships have:
    a representative assistant. Someone who greets you when you walk in, shows you around each model and gives you the description you need to choose what to buy. That is you for the codebase. We have generated descriptive way points for the user to coherently go through and familiarize with the spine of the codebase.
    Think of it this way, these way points are the car models the user needs to see. Before you show them the car models, you need to show them the car brand, and what the character of the brand is. You need to create an intro like that. 1-3 paragraphs depending on the size of the codebase.
    In the intro you have to:
    1. Describe what the codebase does, what the full product is, how it is being used
    2. Provide an overview of the codebase that is coherent with the waypoints you receive. THe intro should touch on core processes, and the waypoints should be the specific descriptions for them.
    3. Write it in a way the user can digest. The user is new, and is using CoTran because they are overwhelmed by all the new libraries, tools, syntax. If you just explain it as is, its going to make them more overwhelmed. Just use plain language so the user can take in what the codebase is and not get overwhelmed by the specifics.
    
    **OUTPUT FORMAT: The output should be in JSON, with only a "text" field. No markdown, no code block, just raw JSON.**"""
   
    content = ""
    query_content = ""
    pyfiles = walk_repo(request.repo_path)
    for file in pyfiles:
        query_content += file
        query_content += "\n"
    readme_path = os.path.join(request.repo_path, "README.md")
    
    with open(readme_path, "r", encoding="utf-8") as readfile:
                readme = readfile.read()
    query_content += readme
    message1 = client.messages.create(max_tokens = 1024,
                                     messages = [{"role":"user", "content": "Here are the file paths to all the files in the codebase and the readme for the codebase:\n\n"+query_content+"\n\nCreate some queries based on these paths and the readme that capture the spine of the codebase, and would allow for the user to feel more familiar with exploring and navigating"}],
                                     model = "claude-sonnet-4-6",
                                     system = query_prompt)
    for s in ast.literal_eval(message1.content[0].text):
        query_response = test_query(s)
        for match in query_response.matches:
            matchmeta = "File: "+match.metadata['path']+"\n"+"Line: "+str(match.metadata['start'])+"\n"+"Code: "+match.metadata['text']+"\n"+"-------"
            content += matchmeta
    
    message2 = client.messages.create(max_tokens = 1024,
                                     messages = [{"role":"user", "content": "Here is relevant code from the codebase:\n\n" + content + "\n\nGenerate the waypoints of the codebase that the user can navigate to familarize with the codebase enough to begin exploration and building."}],
                                     model = "claude-sonnet-4-6",
                                     system = sys_prompt)
    message3= client.messages.create(max_tokens = 1024,
                                     messages = [{"role":"user", "content": "Here are a bunch of way points that coherently describe the spine of the codebase:"+ message2.content[0].text+"Your job is to make an intro for these waypoints and the codebase. You must 1. Say what the codebase is in plain lanugage, 2. Define the 3-4 core concepts the waypoints will reference that a user may not know just from reading it the first tiem, 3. Set up the mental model so every waypoint feels like oh, 'that thing they mentioned'"}],
                                     model = "claude-sonnet-4-6",
                                     system = sys_prompt2)
    
    return {"intro": json.loads(message3.content[0].text), "waypoints": json.loads(message2.content[0].text)}