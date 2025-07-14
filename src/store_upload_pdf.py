import tempfile
from chromadb import Client
from chromadb.utils import embedding_functions
from load_pdf import load_pdf_text
from chunk_text import chunk_text

def store_uploaded_pdf(uploaded_file, collection_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    print("Using in-memory ChromaDB (Client)")
    text = load_pdf_text(tmp_path)
    chunks = chunk_text(text)

    client = Client()
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-mpnet-base-v2"
    )
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embedding_fn)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{uploaded_file.name}-{i}"],
            metadatas=[{"source": uploaded_file.name, "chunk_index": i}]
        )

    return len(chunks)

def list_chroma_collections():
    client = Client()
    return [col.name for col in client.list_collections()]


