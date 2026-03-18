from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
from document_loader import load_document
from embeddings import get_embeddings
from vector_store import build_index, clear_index
from rag_pipeline import get_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../data/uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file.filename.split(".")[-1].lower()
    if ext == "pdf":
        doc_type = "pdf"
    elif ext in ["docx", "doc"]:
        doc_type = "docx"
    else:
        return JSONResponse({"error": "Unsupported file type"}, status_code=400)

    documents = load_document(file_path, doc_type)
    embeddings = get_embeddings([d["text"] for d in documents])
    build_index(documents, embeddings)

    return {"message": f"{file.filename} uploaded and indexed successfully"}


@app.post("/upload_url")
async def upload_url(url: str = Form(...)):
    documents = load_document(url, "url")

    if not documents:
        return JSONResponse({"error": "Could not extract content from URL"}, status_code=400)

    embeddings = get_embeddings([d["text"] for d in documents])
    build_index(documents, embeddings)

    return {"message": f"URL indexed successfully"}


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    if not question.strip():
        return JSONResponse({"error": "Question cannot be empty"}, status_code=400)

    result = get_answer(question)
    return result


@app.post("/clear")
async def clear():
    clear_index()
    return {"message": "Index cleared"}