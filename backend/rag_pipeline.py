from document_loader import load_pdf, load_docx, load_url
from utils.chunking import chunk_text
from embeddings import get_embeddings
from vector_store import create_index


def process_document(file_path, file_type):
    
    if file_type == "pdf":
        text = load_pdf(file_path)

    elif file_type == "docx":
        text = load_docx(file_path)

    elif file_type == "url":
        text = load_url(file_path)

    chunks = chunk_text(text)

    embeddings = get_embeddings(chunks)

    index = create_index(embeddings)

    return chunks, index