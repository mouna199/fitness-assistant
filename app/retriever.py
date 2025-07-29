import minsearch
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.models import Distance, VectorParams

def build_minsearch_index(documents):
    index = minsearch.Index(
        text_fields=[
            'exercise_name', 'type_of_activity', 'type_of_equipment',
            'body_part', 'type', 'muscle_groups_activated', 'instructions'
        ],
        keyword_fields=[]
    )
    index.fit(documents)
    return index

def search_minsearch(index, query, k=5):
    return index.search(query=query, num_results=k)

def setup_qdrant(client, collection_name, embeddings, documents):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=embeddings.shape[1], distance=Distance.COSINE),
    )
    points = [
        PointStruct(id=i, vector=embeddings[i], payload=documents[i])
        for i in range(len(documents))
    ]
    client.upsert(collection_name=collection_name, points=points)

def search_qdrant(client, collection_name, model, query, k=3):
    q_emb = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    results = client.search(
        collection_name=collection_name,
        query_vector=q_emb,
        limit=k
    )
    return [hit.payload for hit in results]