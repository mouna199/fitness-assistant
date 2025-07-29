from sentence_transformers import SentenceTransformer

def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def embed_documents(model, documents, prepare_fn):
    texts = [prepare_fn(doc) for doc in documents]
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=True, normalize_embeddings=True)