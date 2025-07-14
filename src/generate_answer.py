import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer_stream(query, context_chunks, metadatas=None):
    context = ""
    for i, chunk in enumerate(context_chunks):
        meta = metadatas[i] if metadatas and i < len(metadatas) else {}
        source = meta.get("source", "unknown")
        index = meta.get("chunk_index", i)
        context += f"[Source: {source}, Chunk {index}]\n{chunk}\n\n"

    prompt = f"""You are a helpful assistant. Answer the question using only the context provided below.
Cite sources in square brackets like this: [Source: filename.pdf, Chunk 2].
Only use the information from the context — do not make up answers.
If the answer is not present, reply: "Sorry! I couldn't get the answer to your question from the document you uploaded."

Context:
{context}

Question: {query}

Answer (with source citations):
"""


    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a concise and helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
        "stream": True
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        stream=True
    )

    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8").replace("data: ", "")
            if line.strip() == "[DONE]":
                break
            try:
                data = json.loads(line)
                delta = data["choices"][0]["delta"]
                content = delta.get("content", "")
                yield content
            except Exception as e:
                print("Stream error:", e)
