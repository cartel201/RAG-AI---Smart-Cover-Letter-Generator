from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, chat
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma  # FIX: correct import
from langchain_community.embeddings import OllamaEmbeddings
from app.generator import generate  # FIX: single import
from app.vectordb import embed, get_vectordb_for_user



app = FastAPI(title="FastAPI Ollama RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"msg": "RAG is running"}

