from sentence_transformers import SentenceTransformer

# Load model once when the app starts — not every time we call the function
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    # For a single string — used when embedding a question
    return model.encode(text, convert_to_numpy=True)


def get_embeddings(text_list):
    # For a list of strings — used when embedding all chunks
    return model.encode(text_list, convert_to_numpy=True)
