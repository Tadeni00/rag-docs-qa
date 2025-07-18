import os
import tempfile
import streamlit as st
from chromadb import Client
from chromadb.utils import embedding_functions
from src.generate_answer import generate_answer_stream
from src.utils import clean_collection_name
from src.utils import clean_pycache
from src.store_upload_pdf import store_uploaded_pdf, list_chroma_collections
from src.retrieve_chunks import retrieve_chunks
from src.utils import export_answer_to_pdf


# Streamlit UI

st.set_page_config(page_title="🧠 RAG QA", layout="wide")

st.title("📄 Ask Your Documents")
st.markdown("Type a question based on your uploaded or embedded documents.")
st.markdown("---")

# PDF Upload
st.header("📤 Upload a PDF")

raw_collection_name = st.text_input("🗂️ Write the collection name you want to store in below:", value="uploaded-docs")
collection_name = clean_collection_name(raw_collection_name)

uploaded_file = st.file_uploader("Choose a PDF from your device", type="pdf")

if uploaded_file and st.button("➕ Add to Collection"):
    with st.spinner("Storing in ChromaDB..."):
        num_chunks = store_uploaded_pdf(uploaded_file, collection_name)
        st.success(f"✅ Stored {num_chunks} chunks in `{collection_name}` collection.")
        st.session_state["collections"] = list_chroma_collections()  # Refresh list

# Question Answering Section
st.markdown("---")
st.header("🔍 Ask a Question")

# Load collection list
if "collections" not in st.session_state:
    st.session_state["collections"] = list_chroma_collections()

collections = st.session_state["collections"]
selected_collection = st.selectbox("Select a collection to query:", collections)

query = st.text_input("❓ Enter your question:")

if st.button("Generate Answer") and query:
    with st.spinner("🔍 Retrieving context..."):
        chunks, metadatas = retrieve_chunks(query, collection_name=selected_collection)

    st.markdown("### 🤖 Answer")
    answer_placeholder = st.empty()

    with st.spinner("🤖 Generating answer..."):
        full_response = ""
        for token in generate_answer_stream(query, chunks, metadatas):
            full_response += token
            answer_placeholder.markdown(full_response)

    pdf_path = export_answer_to_pdf(full_response, query)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download Answer as PDF",
            data=f,
            file_name="answer.pdf",
            mime="application/pdf"
    )

    with st.expander("📄 Show Retrieved Chunks"):
        for i, chunk in enumerate(chunks):
            st.markdown(f"**Chunk {i+1}:**\n\n{chunk}")

