"""
Step 2 - Chunk Documents
========================

What this does : Splits long pages into smaller overlapping chunks
what you learn : Why chunking matters for retrieval accuracy

Run: Python step2_chunk.py
"""


import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path


DATA_DIR = Path(__file__).parent/'data'

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Load All PDFs


all_documents = []

for filename in sorted(os.listdir(DATA_DIR)):
    if filename.endswith(".pdf"):
        filepath = os.path.join(DATA_DIR,filename)
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        all_documents.extend(pages)

print(f"Loaded {len(all_documents)}  Pages from {DATA_DIR}\n")


splitter = RecursiveCharacterTextSplitter(
    chunk_size= CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP,
    separators= ["\n\n", "\n", "."," ",""]

)

chunks = splitter.split_documents(all_documents)

print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP} \n")


for i,chunk in enumerate(chunks[:3]):
    source = os.path.basename(chunk.metadata['source'])
    page = chunk.metadata['page'] + 1
    print(f'----Chunk {i +1 } | {source}, Page {page} | {len(chunk.page_content)} chars---')
    print(chunk.page_content[:200] + "...\n")