import faiss
import numpy as np


def create_index(embeddings):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index


def search_index(index, query_embedding, k=3):
    distances, indices = index.search(query_embedding, k)
    return indices