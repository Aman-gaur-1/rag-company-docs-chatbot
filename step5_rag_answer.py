"""
Step 5 — Full RAG: Retrieve + Generate Answer
==============================================
What this does : Finds relevant chunks → sends to LLM → returns answer with sources
What you learn : The complete RAG pipeline — retrieval + generation

Run:  python step5_rag_answer.py
Needs: step3 must be run first (creates the Pinecone index)
"""

import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq



os.environ["NVIDIA_API_KEY"] = ""
os.environ["PINECONE_API_KEY"] = ""
os.environ["GROQ_API_KEY"] = ""

INDEX_NAME = "rag-index"
TOP_K = 3


embeddings = NVIDIAEmbeddings(
    model="nvidia/nemotron-3-embed-1b",
    truncate="END",
)

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings,
)

print(f"Connected to Pinecone index '{INDEX_NAME}'\n")


llm = ChatGroq(
    model = "qwen/qwen3.8-27b",
    temperature=0.2
)



def format_doc(docs):
        """Add [filename, Page X] before each chunk so the LLM can cite sources."""

        formatted = []

        for doc in docs:
            source = os.path.basename(doc.metadata['source'])
            page = doc.metadata['page'] + 1
            formatted.append(f'[{source}, Page {page}\n {doc.page_content}')

        return "\n\n---\n\n".join(formatted)

question = "What is the employee leave policy?"
print(f"Question: {question}\n")


docs = vectorstore.similarity_search(question, k=TOP_K)


context = format_doc(docs)

prompt = f"""You are a helpful assistant that answers questions using ONLY the provided context.

Rules:
1. Answer based ONLY on the context below
2. IF the answer is not in the context, say "I don't know based on the available documents.
3. Keep the answer clear and concise
4. Cite the source documents and page number for each fact

Context:
{context}

Question: {question}

Answer: """


response = llm.invoke(prompt)

print("Answer: ", response.content)


print("\n ----Source----")

for i, doc in enumerate(docs, 1):
    source = os.path.basename(doc.metadata['source'])
    page = doc.metadata['page'] + 1
    print(f" {i}. {source}, Page {page}")


more_questions = [
    "What is the refund policy?",
    "How should I report a security incident?",
    "What is the salary structure?",      # not in docs — tests hallucination guard
]

for q in more_questions:
    print(f"Question: {q}\n")
    docs = vectorstore.similarity_search(q,k=TOP_K)
    context = format_doc(docs)
    prompt = f"""You are a helpful assistant that answers questions using ONLY the provided context.

    Rules:
    1. Answer based ONLY on the context below
    2. IF the answer is not in the context, say "I don't know based on the available documents.
    3. Keep the answer clear and concise
    4. Cite the source documents and page number for each fact

    Context:
    {context}

    Question: {q}

    Answer: """

    response = llm.invoke(prompt)

    print("Answer: ", response.content)
    print("\n" + "-" * 60 + "\n")


















