from pypdf import PdfReader
from docx import Document
import trafilatura


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page_num, page in enumerate(reader.pages):
        text += page.extract_text() + "\n"

    return text


def load_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text


def load_url(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text