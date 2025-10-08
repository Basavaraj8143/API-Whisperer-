import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import google.generativeai as genai
from config import GEMINI_API_KEY

# ---------- CONFIG ----------
EMBEDDINGS_FILE = 'output/chunks.json'
FAISS_INDEX_FILE = 'output/faiss_index.bin'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
TOP_K = 5  # Number of chunks to retrieve

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ---------- Load Chunks ----------
with open(EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
    chunks_data = json.load(f)  # no ['chunks']

chunks_texts = [chunk['text'] for chunk in chunks_data]
chunks_meta = [
    {
        "id": c["id"],
        "title": c["title"],
        "source": c["source"]
    }
    for c in chunks_data
]

# ---------- Load Embedding Model ----------
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
dimension = 384  # MiniLM-L6-v2 embedding size

# ---------- Load or Build FAISS Index ----------
if os.path.exists(FAISS_INDEX_FILE):
    print("[*] Loading FAISS index...")
    index = faiss.read_index(FAISS_INDEX_FILE)
else:
    print("[*] Building FAISS index...")
    embeddings = np.array([embedding_model.encode(text) for text in chunks_texts]).astype('float32')
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, FAISS_INDEX_FILE)
    print(f"[+] FAISS index built and saved → {FAISS_INDEX_FILE}")

# ---------- RAG: Answer Question ----------
def answer_question(query, top_k=TOP_K):
    # 1️⃣ Retrieve top-k relevant chunks
    query_vector = embedding_model.encode([query]).astype('float32')
    D, I = index.search(query_vector, top_k)
    retrieved_chunks = [chunks_texts[idx] for idx in I[0]]
    sources = [chunks_meta[idx]['source'] for idx in I[0]]

    # Handle potential infinity in similarity scores
    similarity_scores = np.clip(D[0], -1e6, 1e6)

    # 2️⃣ Build context
    context = "\n\n".join(retrieved_chunks)

    # 3️⃣ System prompt for Gemini
    system_prompt = f"""
You are API Guardian, an expert assistant for API documentation.

Context from documentation:
{context}

Rules:
1. Answer based ONLY on the provided context.
2. If unsure, say "I don't have enough information".
3. Include code examples when available.
4. Cite source URLs.

User Question: {query}
"""

    # 4️⃣ Call Gemini API
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content(
            system_prompt,
            generation_config={
                'temperature': 0.3,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048
            }
        )
        answer_text = response.text
    except Exception as e:
        answer_text = f"Error generating response: {str(e)}"

    # Confidence metric
    confidence = float(np.mean(similarity_scores))
    if not np.isfinite(confidence):
        confidence = 0.0

    return {
        "answer": answer_text,
        "sources": sources,
        "confidence": confidence
    }

# ---------- Example Test ----------
if __name__ == "__main__":
    query = "How do I create a new user?"
    result = answer_question(query)
    print("\nAnswer:\n", result['answer'])
    print("\nSources:\n", result['sources'])
    print("\nConfidence:", result['confidence'])
