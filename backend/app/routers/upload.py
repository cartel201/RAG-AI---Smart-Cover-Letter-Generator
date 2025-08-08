# app/routers/upload.py

from fastapi import APIRouter, UploadFile, Form, File
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
import fitz  # PyMuPDF
from app.routers.extract_metadata import extract_metadata 
from app.generator import set_user_metadata  # import this


# ✅ This is the correct import to create DB
from app.vectordb import create_vectordb_from_text

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), user_id: str = Form(...)):
    pdf_bytes = await file.read()
    text, metadata = extract_metadata(pdf_bytes)

    # ✅ Cache metadata for generator
    set_user_metadata(user_id, metadata)

    create_vectordb_from_text(text, user_id)
    return {"message": f"✅ Vector DB created for {user_id}", "metadata": metadata}