from openai import OpenAI
import tree_sitter
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser((PY_LANGUAGE))
client = OpenAI()
pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))
index = pc.Index("cotran-v1")

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

def get_openai_embeddings(chunks):
    #generate a list of vector embeddings from the list of chunks
    vectors = []
    for chunk in chunks:
        if len(chunk) > 8000:
            chunk = chunk[:8000]
        print(len(chunk))
        response = client.embeddings.create(model = "text-embedding-3-small",
                                            input = chunk)
        vectors.append(response.data[0].embedding)
    return vectors

def upsert_to_pinecone(chunks, vectors):
    #update and insert vectors in to pinecone db
    if not pc.has_index("cotran-v1"):
        pc.create_index(name = "cotran-v1", dimension = 1536, metric = "cosine",
                        spec=ServerlessSpec(cloud = "aws", region = "us-east-1"))
    vectors_to_upsert = []
    for i, vector in enumerate(vectors):
        upsert = {"id": f"chunk-{i}", "values": vector, "metadata": {"text": chunks[i].decode()}}
        vectors_to_upsert.append(upsert)
    upsert_response = index.upsert(vectors = vectors_to_upsert)
    return upsert_response

def test_query(query):
    #querying through pinecone db and finding top 3 most similar
    vector = get_openai_embeddings([query])
    query_response = index.query(vector = vector[0], top_k = 3,
                                 include_values = False, include_metadata = True)
    return query_response
    

if __name__ == "__main__":
    files = walk_repo("/Users/donghoon/Desktop/ct_home/fastapi")
    for file in files:
        chunks = parse_chunks(file)
        if chunks:
            vectors = get_openai_embeddings(chunks)
            upsert_response = upsert_to_pinecone(chunks, vectors)