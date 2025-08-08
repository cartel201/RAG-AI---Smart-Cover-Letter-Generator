from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import requests
import os

from app.generator import generate
from app.vectordb import get_vectordb_for_user


router = APIRouter()


@router.post("/init-db")
async def init_vector_db(user_id: str = "default"):
    sample_text = """
    Madhup Singh is a Python developer with experience in FastAPI, LangChain, RAG, Ollama, and backend systems.
    He has worked on resume parsing, job recommendation systems, and AI agents.
    """
    from app.vectordb import create_vectordb_from_text
    chunks = create_vectordb_from_text(sample_text, user_id)
    return {"message": f"✅ Created vector DB for {user_id} with {chunks} chunks"}


class CoverLetterRequest(BaseModel):
    job_description: str
    user_id: str = "default"
    tone: str = "formal"

@router.post("/cover-letter")
async def generate_cover_letter(req: CoverLetterRequest):
    try:
        vdb = get_vectordb_for_user(req.user_id)
        letter = generate(req.job_description, req.user_id, req.tone, OllamaEmbeddings(model="nomic-embed-text"), vdb)
        return {"letter": letter}
    except Exception as e:
        return {"error": f"❌ Error generating letter: {str(e)}"}



class Query(BaseModel):
    user_id: str
    question: str

@router.post("/chat")
async def rag_chat(query: Query):
    try:
        embeddings = OllamaEmbeddings(model="llama3")
        db_path = f"chroma_db/{query.user_id}"

        if not os.path.exists(db_path):
            raise HTTPException(status_code=404, detail="No data found for this user.")

        vectordb = Chroma(persist_directory=db_path, embedding_function=embeddings)
        docs = vectordb.similarity_search(query.question, k=4)

        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"""Answer the question based only on the context below.

Context:
{context}

Question:
{query.question}
"""

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })

        result = response.json()
        return {
            "answer": result.get("response", "No response"),
            "sources": [doc.metadata for doc in docs]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))