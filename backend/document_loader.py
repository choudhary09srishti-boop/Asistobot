from pypdf import PdfReader
from docx import Document
import trafilatura


def load_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "text": text.strip(),
                "page": page_num + 1,
                "source": file_path
            })

    return pages


def load_docx(file_path):
    doc = Document(file_path)
    pages = []

    for para_num, para in enumerate(doc.paragraphs):
        if para.text.strip():
            pages.append({
                "text": para.text.strip(),
                "page": 1,
                "para": para_num + 1,
                "source": file_path
            })

    return pages


def load_url(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)

    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    pages = []

    for para_num, para in enumerate(paragraphs):
        pages.append({
            "text": para,
            "page": 1,
            "para": para_num + 1,
            "source": url
        })

    return pages


def load_document(file_path_or_url, doc_type):
    if doc_type == "pdf":
        return load_pdf(file_path_or_url)
    elif doc_type == "docx":
        return load_docx(file_path_or_url)
    elif doc_type == "url":
        return load_url(file_path_or_url)
    else:
        return []
