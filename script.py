import pandas as pd 
import minsearch
from dotenv import dotenv_values
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct



path = 'data/data.csv'
def get_data(path):
    df = pd.read_csv(path,sep=',')
    documents = df.to_dict(orient='records')
    return documents


def fit_document(documents):
    index = minsearch.Index(
        text_fields=['exercise_name', 'type_of_activity', 'type_of_equipment', 'body_part',
           'type', 'muscle_groups_activated', 'instructions'],
        keyword_fields=[]
    )
    index.fit(documents)
    return index



q = "give me exercice for hamstrings"
documents = get_data(path)
index = fit_document(documents)

def search(q):
    results = index.search(
        query = q,
        num_results = 5
    )
    return results

env_vars = dotenv_values(".envrc")  # charge les variables du .envrc
api_key = env_vars["OPENAI_API_KEY"]
def llm(prompt, model = 'gpt-4o-mini'):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model = model,
        messages = [{"role":"user","content":prompt}],
    )   
    return response.choices[0].message.content

prompt_template = """
You are a fitness coach.Answer the QUESTION based on the CONTEXT.
Use only the facts from the CONTEXT when answering the QUESTION.
If the CONTEXT doesn't contain the answer, output I don't know.
QUESTION: {question}
CONTEXT:{context}
"""

entry_template = """
exercise_name: {exercise_name}
type_of_activity: {type_of_activity}
type_of_equipment: {type_of_equipment}
body_part: {body_part}
type: {type}
muscle_groups_activated: {muscle_groups_activated}
instructions: {instructions}
""".strip()


def build_prompt(results,q):
    context = ""
    for doc in results:
        context = context + entry_template.format(**doc) + "\n\n"
    prompt = prompt_template.format(question=q, context=context)
    return prompt

def rag(q):
    results = search(q)
    print(results)
    prompt = build_prompt(results,q)
    response = llm(prompt)
    return response

response = rag(q)
print(response)



client = QdrantClient(url="http://localhost:6333")


def prepare_text(doc):
    return f"{doc['exercise_name']} , {doc['type_of_activity']}, {doc['type_of_equipment']} , {doc['body_part']} , {doc['type']} , {doc['muscle_groups_activated']} , {doc['instructions']}"
text = [prepare_text(doc) for doc in documents]

from sentence_transformers import SentenceTransformer

# 1. Charger un modèle d'embedding léger
model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")

# 3. Génération des vecteurs (embeddings)
embeddings = model.encode(
    text,
    show_progress_bar=True,     # Affiche la barre de chargement
    convert_to_numpy=True,      # Retourne des vecteurs NumPy
    normalize_embeddings=True   # (Optionnel) pour normaliser (utile si tu utilises cosine)
)


embeddings.shape
# Create a collection
from qdrant_client.models import Distance, VectorParams

client.recreate_collection(
    collection_name="fitness_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

points = [
    PointStruct(
        id=i,
        vector=embeddings[i],
        payload=documents[i]
    )
    for i in range(len(documents))
]

client.upsert(
    collection_name="fitness_collection",
    points=points
)


def search_with_qdrant(q):
    q_emb = model.encode(
    q,
    convert_to_numpy=True,
    normalize_embeddings = True
)
    search_result = client.search(
        collection_name="fitness_collection",
        query_vector=q_emb,
        limit = 3
    )

    return [hit.payload for hit in search_result]


def rag_qdrant(q):
    results = search_with_qdrant(q)
    prompt = build_prompt(results,q)
    response = llm(prompt)
    return response

rag_response = rag_qdrant("give me exercice for abs")



