"""
Step 1 - Load Documents
=======================

What this does : Reads all pdf files from the data/folder
what you learn : How langchain turn pdfs into documents objects

Run: python step1_load.py
"""
from pathlib import Path
import os
from langchain_community.document_loaders import PyPDFLoader

# DATA_DIR = "data"
DATA_DIR = Path(__file__).parent


all_documents = []

for filename in sorted(os.listdir(DATA_DIR)):
    if filename.endswith(".pdf"):
        filepath = os.path.join(DATA_DIR,filename)
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        all_documents.extend(pages)
        print(f' Loaded: {filename}---> {len(pages)} pages')

print(f'\n Total documents loaded: {len(all_documents)} pages')


print("\n ---Preview of first page----")
doc = all_documents[0]

print(f"Source  :    {doc.metadata['source']}")
print(f'Page    :    {doc.metadata['page'] +1}')
print(f"Content  :   {doc.page_content[:300]}.....")





