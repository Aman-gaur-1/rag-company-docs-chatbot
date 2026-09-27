# Step 3: Embeddings and Vector Store

This step turns each chunk into a numeric embedding and saves the vectors in a Pinecone Vector Store for later search.

## Goal

Create a serverless Pinecone index called `rag-index` and upload an embedding for every chunk.

## Why this step exists

Text needs to be represented in a form that supports meaning-based comparison. An embedding is like a location for a passage on a map of meanings. Passages about a similar topic tend to have nearby vectors.

The NVIDIA model in the code returns 2,048 numbers for each text. Pinecone needs an index with the same dimension so each vector fits. The code sets `dimension=2048`; [NVIDIA's model page](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-embed-1b) lists the same output size.

The index uses the `cosine` similarity metric. In one line: cosine compares the direction of two vectors to estimate how similar their meanings are. The code creates a serverless index, which means Pinecone manages the serving infrastructure rather than asking this script to manage fixed servers.

## Full code

{% code title="step3_embed_store.py" lineNumbers="true" %}
```python
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


os.environ["NVIDIA_API_KEY"] = "YOUR_NVIDIA_API_KEY"
os.environ["PINECONE_API_KEY"] = "YOUR_PINECONE_API_KEY"

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
```
{% endcode %}

{% hint style="danger" %}
The current script deletes `rag-index` if it already exists, then creates it again. That removes the old index and its data. Review this behavior before running step 3 against an index you need.
{% endhint %}

## Line-by-line explanation

### Imports and configuration

- `os` reads environment variables, and `time` pauses between Pinecone operations.
- `PyPDFLoader` and `RecursiveCharacterTextSplitter` repeat the load-and-chunk steps so this script can run on its own.
- `NVIDIAEmbeddings` creates the vectors; `PineconeVectorStore` writes LangChain documents to Pinecone.
- The `openai` import is present in the source but is not used later in the file.
- `Pinecone` manages indexes. `ServerlessSpec` describes the cloud and region for the new index.
- `DATA_DIR` points to the PDFs. `INDEX_NAME` is `rag-index`; the chunk values match step 2.
- API credentials are omitted from the code shown here. The checked-in file contains credential assignments. Never copy those values into another project.

### Load, split, and create the index

The first loop reads all PDFs and page documents, then the splitter recreates the 1,000-character chunks with 200-character overlap. The print statements announce the page and chunk totals.

`Pinecone(api_key=...)` creates an API client. The code lists existing indexes, checks whether `rag-index` exists, deletes it if so, and waits five seconds. It then creates an index with dimension 2,048, cosine similarity, and an AWS serverless specification in `us-east-1`. The loop waits one second at a time until Pinecone reports the index is ready.

### Embed and upload

`NVIDIAEmbeddings` selects `nvidia/nemotron-3-embed-1b`. The source spells the truncation argument `trucate`, while step 4 and step 5 use `truncate`. Treat this as a source typo and verify the installed integration's accepted option before using it.

`PineconeVectorStore.from_documents` embeds each chunk and upserts its text and metadata. The final print lines report the vector count and completion.

## Run it

~~~bash
python step3_embed_store.py
~~~

### Expected output

The script prints status lines in this order. The delete line appears only when the index already exists; counts and the data path depend on the run.

~~~text
Loaded <page count> Pages from <data path>
Split into <chunk count> chunks (size=1000, overlap=200
Deleted old index rag-index
Created Pinecone index rag-index
Index is ready!!
Creating embeddings and uploading to Pinecone.....
Stored <chunk count> vectors in Pinecone index rag-index
DONE!!
~~~

<!-- TODO: paste real output from the video -->

The script was not run because the file contains saved credentials and deletes an existing index before recreating it.

## Common mistakes

- Pinecone index name does not match `rag-index`.
- Index dimension differs from the embedding model's 2,048-dimensional output.
- Running the script again deletes an index you meant to keep.
- Credential values are missing, invalid, or placed in a file the script never reads.

## Check yourself

<details>
<summary>Answer</summary>

1. **What is an embedding?** A numeric representation of text that lets the system compare meanings.
2. **Why set the dimension to 2,048?** Each vector from this NVIDIA model contains 2,048 values.
3. **What does the similarity metric do?** It tells Pinecone how to compare vectors.

</details>

[Next: Step 4, retrieval](08-retrieval.md)
