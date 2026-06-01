import openai
import tree_sitter
import pinecone
import os
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser((PY_LANGUAGE))

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

def walk_node(node, chunks):
    #walks through all nodes recursively through child nodes
    if node.type == "function_definition" or node.type == "class_definition":
        chunks.append(node.text)
    for child_node in node.children:
        walk_node(child_node, chunks)

    return chunks

def parse_chunks(file):
    #takes a file and reads its content
    #parse the encoded contents of the file in to a tree
    #traverses that tree and collects the chunks
    with open(file) as f:
        contents = f.read()
    tree = parser.parse(contents.encode())
    curr = tree.root_node
    chunks = []
    chunks = walk_node(curr, chunks)
    return chunks

if __name__ == "__main__":
    files = walk_repo("/Users/donghoon/Desktop/ct_home/fastapi")
    chunks = parse_chunks(files[0])

    print(chunks)
