from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, uuid, requests
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = FastAPI(title="RAG PDF Assistant with Ollama")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Ollama Embeddings & Chroma DB ===
embedder = OllamaEmbeddings(model="nomic-embed-text")
vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embedder)

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...), user_id: str = "default"):
    filepath = f"./uploads/{uuid.uuid4()}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(filepath)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["user"] = user_id

    vectordb.add_documents(chunks)
    vectordb.persist()

    return {"msg": f"✅ Uploaded and indexed {len(chunks)} chunks."}

class Query(BaseModel):
    user_id: str
    question: str

@app.post("/api/chat")
async def chat(q: Query):
    results = vectordb.similarity_search_with_score(q.question, k=4)
    if not results:
        return {"answer": "No relevant content found.", "sources": []}

    documents = [doc.page_content for doc, _ in results]
    context = "\n\n".join(documents)

    prompt = f"""You are a helpful AI career assistant. Use the context below to answer the question.

Context:
{context}

Question: {q.question}
"""

    answer = query_ollama(prompt)
    return {"answer": answer, "sources": [doc.metadata for doc, _ in results]}

def query_ollama(prompt, model="llama3"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
