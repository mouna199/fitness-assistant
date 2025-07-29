from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.utils import load_data, prepare_text
from app.embedder import get_model, embed_documents
from app.retriever import (
    build_minsearch_index, search_minsearch,
    setup_qdrant, search_qdrant
)
from app.rag_pipeline import rag
from qdrant_client import QdrantClient


class QueryInput(BaseModel):
    query: str
    
path = "data/data.csv"
documents = load_data(path)

# Backend: 'minsearch' or 'qdrant'
BACKEND = "qdrant"

if BACKEND == "minsearch":
    index = build_minsearch_index(documents)
    search_fn = lambda q: search_minsearch(index, q)

elif BACKEND == "qdrant":
    model = get_model()
    embeddings = embed_documents(model, documents, prepare_text)
    client = QdrantClient("http://localhost:6333")
    setup_qdrant(client, "fitness_collection", embeddings, documents)
    search_fn = lambda q: search_qdrant(client, "fitness_collection", model, q)




app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def query_endpoint(payload: QueryInput):
    user_query = payload.query
    result = rag(user_query, search_fn)
    return {"answer": result}

# Test function for direct execution
if __name__ == "__main__":
    test_query = "give me exercise for hamstrings"
    print(f"Query: {test_query}")
    response = rag(test_query, search_fn)
    print(f"Response: {response}")
