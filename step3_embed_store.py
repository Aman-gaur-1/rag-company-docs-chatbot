"""
Step 3 — Create Embeddings & Store in Pinecone
===============================================
What this does : Converts every chunk into a vector and stores in Pinecone
What you learn : Embeddings turn text into numbers that capture meaning

Run:  python step3_embed_store.py
"""


import os, time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_pinecone import PineconeVectorStore
from openai import embeddings, vector_stores
from pinecone import Pinecone, ServerlessSpec
from pathlib import Path


os.environ["NVIDIA_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "pcsk_3kLLLK_BnazGa3jHgiU7ybV7Pi34kkK9QsMqQbk4ejGCfA8aZ1AcqwqvdkC4oBT8tyHcfo"

DATA_DIR = Path(__file__).parent/'data'
INDEX_NAME = "rag-index"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# 1 - Load all PDFs
all_documents = []

for filename in sorted(os.listdir(DATA_DIR)):
    if filename.endswith(".pdf"):
        filepath = os.path.join(DATA_DIR,filename)
        loader = PyPDFLoader(filepath)
        pages = loader.load()
        all_documents.extend(pages)

print(f"Loaded {len(all_documents)}  Pages from {DATA_DIR}\n")

#Split into Chunks

splitter = RecursiveCharacterTextSplitter(
    chunk_size= CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP,
    separators= ["\n\n", "\n", "."," ",""]

)

chunks = splitter.split_documents(all_documents)

print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP} \n")



pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

existing_indexs = [i.name for i in pc.list_indexes()]

if INDEX_NAME in existing_indexs:
    pc.delete_index(INDEX_NAME)
    print(f"Deleted old index {INDEX_NAME}")
    time.sleep(5)

pc.create_index(
    name=INDEX_NAME,
    dimension=2048,
    metric='cosine',
    spec=ServerlessSpec(cloud='aws',region='us-east-1'),
)

print(f'Created Pinecone index {INDEX_NAME}')

while not pc.describe_index(INDEX_NAME).status['ready']:
    time.sleep(1)

print('Index is ready!!')


print("\n Creating embeddings and uploading to Pinecone.....")

embeddings = NVIDIAEmbeddings(
    model= "nvidia/nemotron-3-embed-1b",
    trucate='END'
)


vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=INDEX_NAME
)


print(f'Stored {len(chunks)} vectors in Pinecone index {INDEX_NAME}')
print("DONE!!")



























