# RAG Document QA Assistant

A full-stack RAG (Retrieval-Augmented Generation) application that allows users to upload PDFs, semantically search their contents, and get accurate answers powered by LLaMA 3 (70B) using Groq API. Built with `Streamlit`, `ChromaDB`, and `SentenceTransformers`.

---

## What This App Does

1. Upload PDF documents.
2. Automatically chunk and embed the text using `all-mpnet-base-v2`.
3. Store document chunks in `ChromaDB` with metadata (filename, chunk index).
4. Let users ask natural language questions.
5. Retrieve the most relevant chunks using semantic similarity.
6. Generate answers using `LLaMA 3 (70B)` hosted via Groq.
7. Cite sources (PDF name and chunk number) in the final response.

---

## Project Structure

rag-docs-qa/

├── Dockerfile

├── requirements.txt

├── README.md

├── .dockerignore

├── app.py                     # Main Streamlit entry point

├── src/

│   ├── __init__.py

│   ├── generate_answer.py     # Handles LLM querying (Groq + LLaMA 3)

│   ├── retrieve_chunks.py     # Retrieves similar chunks from ChromaDB

│   ├── store_upload_pdf.py    # Chunks + stores uploaded PDFs into ChromaDB

│   └── utils.py               # Utilities (e.g., clean_collection_name, pycache cleanup)

├── data/

│   └── chroma/                      
           



---

## How It Works

### 1. Upload PDFs
- User uploads a document via Streamlit.
- `load_pdf.py` extracts the full text.
- `chunk_text.py` breaks the text into chunks of 500 tokens.

### 2. Store in ChromaDB
- Each chunk is embedded with `all-mpnet-base-v2`.
- Stored with metadata (source, chunk index) in ChromaDB.
- Each collection is named after the sanitized input (no spaces or special chars).

### 3. Ask Questions
- User types a question and selects the document collection to query.
- `retrieve_chunks.py` computes embedding with `all-mpnet-base-v2` (better retrieval quality).
- Top `k` most similar chunks are returned with their metadata.

### 4. Generate Answer
- `generate_answer.py` constructs a prompt with the retrieved context and citations.
- Sends the prompt to Groq’s `llama3-70b-8192` endpoint with streaming enabled.
- The model responds with an answer and cites sources inline using the metadata.

---

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/tadeni00/rag-docs-qa.git
cd rag-docs-qa

### 2. Create a virtual environmen

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Create a .env file

GROQ_API_KEY=your_groq_api_key_here

### 5. Run the app

streamlit run app.py

## Why Each Component Was Chosen

| Component                 | Reason                                                                  |
|---------------------------|-------------------------------------------------------------------------|
| **ChromaDB**              | Fast, local vector database with persistent client                      |
| **Sentence Transformers** | High-quality semantic embeddings for document chunks                    |
| **all-mpnet-base-v2**     | Used consistently for both storage and query embeddings for performance |
| **Groq + LLaMA 3**        | Blazing fast open-source inference with accurate responses              |
| **Streamlit**             | Minimal, real-time UI for file upload, query, and streaming output      |


## Challenges & Resolutions

| Challenge                                             | Resolution                                                                                           |
|-------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| **1. Collection name validation**                    | Used `clean_collection_name()` to sanitize user input — replaced spaces, removed special chars.     |
| **2. ChromaDB dimension mismatch (e.g. 384 vs 768)** | Ensured the same embedding model (`all-mpnet-base-v2`) is used for both storing and querying.       |
| **3. Streaming from Groq API**                       | Implemented a generator to yield chunks as they arrive. Handled decoding and newline characters.     |
| **4. Chunk metadata not shown**                      | Added `[Source: filename.pdf, Chunk #]` tags in the context and improved prompt clarity.            |
| **5. Missing citations in output**                   | Refined the prompt to explicitly ask the model to cite sources. Boosted consistency in responses.   |
| **6. Duplicate 'Generate Answer' button**            | Removed redundant Streamlit button logic. Only one unified handler now triggers generation.         |


## Planned Improvements

✅ Support for multiple collections

✅ Display chunk citations with answer

✅ Export answer (PDF/Markdown)

✅ Deployment on Streamlit Cloud

⏳ Chunk visualization and highlighting

⏳ Support non-PDF text inputs (like DOCX, TXT)
