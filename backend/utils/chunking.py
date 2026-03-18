from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)


def chunk_documents(documents):
    chunks = []

    for doc in documents:
        parts = splitter.split_text(doc["text"])

        for i, part in enumerate(parts):
            chunks.append({
                "text": part,
                "page": doc.get("page", 1),
                "para": doc.get("para", i + 1),
                "source": doc.get("source", "unknown")
            })

    return chunks
