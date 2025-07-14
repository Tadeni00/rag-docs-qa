from chromadb import Client
from chromadb.utils import embedding_functions

def retrieve_chunks(query, top_k=5, collection_name="dev-docs"):
    client = Client()
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-mpnet-base-v2"
    )
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embedding_fn)
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0], results["metadatas"][0]
