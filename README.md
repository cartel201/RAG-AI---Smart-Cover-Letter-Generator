🧠 Smart AI(RAG) Cover Letter Generator

Generate professional, one-page cover letters by simply uploading your resume and pasting a job description. Powered by LLMs, embeddings, and RAG for precise and contextual results.

## 🚀 Features

- Resume Upload (PDF/DOCX)
- Extracts name, email, phone, address
- Tailored to job description
- Custom tone: Formal, Friendly, Enthusiastic
- Copy letter with animation
- Dark mode support
- LLM runs locally (no API cost!)

## 🔧 Tech Stack

### Backend
- FastAPI
- LangChain
- Ollama (LLaMA3)
- Chroma DB
- PyMuPDF / python-docx
- Regex + RAG Retrieval

### Frontend
- React + TailwindCSS
- Framer Motion
- Lucide React (icons)
- Axios

## 📂 Folder Structure

```
📁 backend/
    └── app/
        ├── routers/
        ├── utils/
📁 frontend/
    └── src/
        ├── components/
```

## 🧠 How it works (RAG)
1. Resume is chunked and embedded (via LangChain + LLaMA3)
2. Stored in Chroma Vector DB
3. On job description input → relevant chunks are retrieved
4. Prompted with job + resume to generate letter

## 🛠️ Installation

```bash
# Backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
npm install
npm run dev

# LLM (Ollama)
ollama run llama3
```
## 📬 Connect

Created by [Madhup Singh](https://www.linkedin.com/in/madhup-singh-04601a283/)  