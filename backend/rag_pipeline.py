import os
from dotenv import load_dotenv
from groq import Groq
from embeddings import get_embedding
from vector_store import search_index
from utils.citation import format_all_citations

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = []


def get_answer(question):
    global chat_history

    # Step 1 — embed the question
    query_embedding = get_embedding(question)

    # Step 2 — search FAISS for top 4 relevant chunks
    relevant_chunks = search_index(query_embedding, k=4)

    if not relevant_chunks:
        return {
            "answer": "No documents uploaded yet. Please upload a PDF, DOCX or URL first.",
            "sources": [],
            "follow_up": ""
        }

    # Step 3 — format citations
    citations = format_all_citations(relevant_chunks)

    # Step 4 — build context from chunks
    context = "\n\n".join([
        f"[{c['label']}]\n{c['text']}"
        for c in citations
    ])

    # Step 5 — build system prompt
    system_prompt = """You are a research assistant. 
Answer the user's question strictly based on the provided document excerpts.
Always mention the source document name and page number when citing information.
If the answer is not found in the documents, say so clearly.
Be concise, accurate and scholarly in tone."""

    # Step 6 — add question to chat history
    chat_history.append({"role": "user", "content": question})

    # Step 7 — build messages for Groq
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Document excerpts:\n{context}\n\nQuestion: {question}"}
    ] + chat_history[-6:]

    # Step 8 — call Groq LLM
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=0.3,
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    # Step 9 — save answer to chat history
    chat_history.append({"role": "assistant", "content": answer})

    # Step 10 — generate follow up question
    follow_up = generate_follow_up(question, answer)

    return {
        "answer": answer,
        "sources": citations,
        "follow_up": follow_up
    }


def generate_follow_up(question, answer):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"Based on this question: '{question}' and answer: '{answer}', suggest one short natural follow-up question the user might want to ask. Return only the question, nothing else."
            }
        ],
        temperature=0.5,
        max_tokens=60
    )
    return response.choices[0].message.content


def clear_history():
    global chat_history
    chat_history = []