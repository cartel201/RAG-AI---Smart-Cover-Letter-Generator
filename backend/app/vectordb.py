from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from typing import List, Tuple
import os
import re

embed = OllamaEmbeddings(model="nomic-embed-text")

# 👤 Extract personal info (optional)
def extract_personal_info(text: str) -> dict:
    name_match = re.search(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", text)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"\+?\d[\d -]{8,}\d", text)
    return {
        "name": name_match.group() if name_match else None,
        "email": email_match.group() if email_match else None,
        "phone": phone_match.group() if phone_match else None,
    }

# ✅ Create vector DB and persist
def create_vectordb_from_text(text: str, user_id: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([Document(page_content=text)])
    persist_dir = os.path.abspath(f"chroma_store/{user_id}")
    os.makedirs(persist_dir, exist_ok=True)

    vectordb = Chroma.from_documents(docs, embed, persist_directory=persist_dir)
    return len(docs)

# ✅ Load vector DB safely
def get_vectordb_for_user(user_id: str):
    persist_dir = os.path.abspath(f"chroma_store/{user_id}")
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"No vector DB found for user: {user_id}")
    return Chroma(persist_directory=persist_dir, embedding_function=embed)
