import os
from tempfile import NamedTemporaryFile
from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

async def parse_file(file) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    tmp = NamedTemporaryFile(delete=False, suffix=ext)
    tmp.write(await file.read())
    tmp.close()
    file_path = tmp.name

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    os.remove(file_path)

    return "\n".join(doc.page_content for doc in docs)

def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

def store_chunks(chunks: List[str], user_id: str, embed, vectordb) -> int:
    docs = [
        Document(page_content=chunk, metadata={"user": user_id})
        for chunk in chunks
    ]
    vectordb.add_documents(docs)
    vectordb.persist()
    return len(docs)
