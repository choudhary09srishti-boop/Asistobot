import faiss
import numpy as np

# In-memory storage for chunks and index
chunk_store = []
faiss_index = None


def build_index(chunks, embeddings):
    global faiss_index, chunk_store

    chunk_store = chunks
    embeddings_np = np.array(embeddings).astype("float32")

    dimension = embeddings_np.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings_np)


def search_index(query_embedding, k=4):
    global faiss_index, chunk_store

    if faiss_index is None:
        return []

    query_np = np.array([query_embedding]).astype("float32")
    distances, indices = faiss_index.search(query_np, k)

    results = []
    for i in indices[0]:
        if i != -1 and i < len(chunk_store):
            results.append(chunk_store[i])

    return results


def clear_index():
    global faiss_index, chunk_store
    faiss_index = None
    chunk_store = []