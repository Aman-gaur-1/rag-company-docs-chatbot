"""
Step 4 — Retrieve Relevant Chunks
==================================
What this does : Takes a question and finds the most similar chunks
What you learn : Semantic search — finding meaning, not just keywords

Run:  python step4_retrieve.py
Needs: step3 must be run first (creates the Pinecone index)
"""

import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_pinecone import PineconeVectorStore


os.environ["NVIDIA_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "pcsk_3kLLLK_BnazGa3jHgiU7ybV7Pi34kkK9QsMqQbk4ejGCfA8aZ1AcqwqvdkC4oBT8tyHcfo"

INDEX_NAME = "rag-index"

embeddings = NVIDIAEmbeddings(
    model= "nvidia/nemotron-3-embed-1b",
    trucate='END'
)


vectorstore = PineconeVectorStore(
    embedding=embeddings,
    index_name=INDEX_NAME
)

print(f'Connected to Pinecone index {INDEX_NAME}\n')

question = "What is the employee leave policy?"
print(f'Question: {question}\n')


result = vectorstore.similarity_search(question, k=3)


print(f'Top 3 Result: \n')

for i, doc in enumerate(result,1):
    source = os.path.basename(doc.metadata['source'])
    page = doc.metadata["page"] + 1
    print(f"---Result {i} | {source}, Page {page} ---")
    print(doc.page_content[:250] + "...\n")
















