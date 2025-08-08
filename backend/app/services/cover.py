from langchain_community.chat_models import ChatOllama


def generate(job_desc, user_id, tone, embed, vdb):
    try:
        # Use retriever from the vectorstore
        retriever = vdb.as_retriever(search_kwargs={"k": 6})
        related_docs = retriever.get_relevant_documents(job_desc)

        # Combine the content from the relevant docs
        resume_bits = "\n\n".join([doc.page_content for doc in related_docs])

        # Prompt template
        template = (
            "Write a {tone} cover letter tailored to this job.\n\n"
            "=== Resume Extract ===\n{resume}\n\n"
            "=== Job Description ===\n{jd}\n\n"
            "The letter should be one page, highlight matching skills, "
            "and end with a courteous sign-off."
        )
        prompt = template.format(tone=tone, resume=resume_bits, jd=job_desc)

        # LLM using Ollama (llama3)
        llm = ChatOllama(model="llama3")
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"❌ Error generating letter: {str(e)}"