import openai
import tree_sitter
import pinecone
import os

def walk_repo(repo):
    #walks through the repo, finds all python files
    #returns the paths as a list
    files = os.walk(repo)
    pyfiles = []
    for file in files:
        for filename in file[2]:
            if filename.endswith(".py"):
                pyfiles.append(os.path.join(file[0], filename))
    return pyfiles