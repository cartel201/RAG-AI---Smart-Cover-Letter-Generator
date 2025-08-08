import re
from datetime import datetime
from langchain_ollama import ChatOllama

# In-memory metadata cache
user_metadata_cache = {}

def set_user_metadata(user_id: str, metadata: dict):
    user_metadata_cache[user_id] = metadata

def get_user_metadata(user_id: str):
    return user_metadata_cache.get(user_id, {})

def extract_company_name(job_desc: str):
    match = re.search(r"at\s+([A-Z][A-Za-z0-9&\-. ]+)", job_desc)
    return match.group(1).strip() if match else "[Company Name]"

def generate(job_desc, user_id, tone, embed, vdb):
    try:
        retriever = vdb.as_retriever(search_kwargs={"k": 4})
        def ask(query):
            docs = retriever.invoke(query)
            return "\n".join([doc.page_content for doc in docs]) if docs else ""

        meta = get_user_metadata(user_id)
        print(f"📌 Cached Metadata for {user_id}: {meta}")

        name = meta.get("name") or ask("What is the candidate's full name?")
        email = meta.get("email") or ask("What is the candidate's email?")
        phone = meta.get("phone") or ask("What is the candidate's phone number?")
        address = meta.get("address") or ask("What is the candidate's address?")
        print(f"{job_desc}")

        # Backup fallback extraction
        full_text = ask("Return the full resume text.")
        if not email or email.lower() == "n/a":
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", full_text)
            email = emails[0] if emails else "N/A"
        if not phone or phone.lower() == "n/a":
            phones = re.findall(r"\b\d{10}\b", full_text)
            phone = phones[0] if phones else "N/A"

        # Extract relevant resume context and skills
        resume_context = ask(job_desc)
        skills = ask("What technologies, libraries, and frameworks does the candidate know?")

        today = datetime.today().strftime("%B %d, %Y")
        company = extract_company_name(job_desc)

        prompt = f"""
Write a detailed and formal one-page cover letter for the role of: {job_desc}.

It should:
- DO NOT include any headers like [Name], [Date], or [Address] at the top.
- DO NOT include the company address block either.
- Start directly with "Dear Hiring Manager," (or if you know the name, use it).
- Be written in a professional tone
- Include specific technologies, tools, libraries, and frameworks the candidate knows relavant to {job_desc}
- Strictly Align with the job description: {job_desc}
- Extract and reflect the candidate’s relevant experience and skills
- Highlight relevant skills and achievements from the resume.
- End with a polite thank-you
- Contain no placeholders like [Your Name], [Email], etc.
- Avoid any duplication or irrelevant repetition

Company: {company}

Resume Extract:
{resume_context}

Extracted Skills:
{skills}

- Use this footer block for the signature:

Sincerely,
{name}
{address}
{phone}
{email}

Avoid adding any introductory lines such as "Here is a cover letter for the role of...". Only return the letter content.
"""

        llm = ChatOllama(model="llama3")
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"❌ Error generating letter: {str(e)}"
