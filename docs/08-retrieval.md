# Step 4: Retrieval

Retrieval embeds a question, searches the Pinecone Vector Store, and returns the three closest chunks.

## Goal

Find the chunks most relevant to the question, “What is the employee leave policy?”

## Why this step exists

The chatbot needs useful source text before it can answer. Semantic search compares the meaning of the question with stored chunk embeddings. This helps when the question uses different words from the document. Keyword search can still be useful, especially for exact names or codes; this project uses vector similarity search.

The setting `k=3` asks the Vector Store for the three most similar chunks. That is called top-k: think of asking a librarian for the three closest matches on the shelf. Here, k is how many search results to return.

## Full code

{% code title="step4_retrieve.py" lineNumbers="true" %}
```python
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


os.environ["NVIDIA_API_KEY"] = "YOUR_NVIDIA_API_KEY"
os.environ["PINECONE_API_KEY"] = "YOUR_PINECONE_API_KEY"

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
```
{% endcode %}

## Line-by-line explanation

### Connect to the index

- `import os` is used to shorten the source paths in output.
- `NVIDIAEmbeddings` embeds the search question using `nvidia/nemotron-3-embed-1b`.
- `PineconeVectorStore` connects that embedding client to `rag-index`.
- The source file assigns API credentials directly. Their values are redacted from this page.
- `INDEX_NAME = "rag-index"` must match the index created in step 3.
- `trucate="END"` is misspelled in this file too. Step 5 uses `truncate`; check the parameter name accepted by your installed package.

### Search and display results

The code connects to the index and prints the fixed question. `similarity_search(question, k=3)` embeds the question and asks Pinecone for three similar documents.

The loop prints each result's rank, source filename, and page. It adds 1 to the stored page index for a reader-friendly citation and prints the first 250 characters of the passage. This script retrieves text only; it does not ask Groq to write an answer.

## Run it

~~~bash
python step4_retrieve.py
~~~

### Expected output

The source prints a connection message, the question, a result heading, and up to three result blocks with the source filename, page, and a short text preview.

~~~text
Connected to Pinecone index rag-index
Question: What is the employee leave policy?
Top 3 Result:
---Result 1 | <filename>, Page <page> ---
<first 250 characters of matching chunk>...
~~~

<!-- TODO: paste real output from the video -->

No search was run because this script contains saved API credentials.

## Common mistakes

- Step 3 has not created the index yet.
- The configured index name is different from `rag-index`.
- Page metadata is absent or has a different key than `source` or `page`.
- A returned chunk is relevant but does not contain the exact answer; retrieval supplies context, not a guarantee.

## Check yourself

<details>
<summary>Answer</summary>

1. **What does top-k mean?** The number of nearest chunks returned; here k is 3.
2. **Does this script generate an answer?** No. It prints retrieved passages.
3. **Why use semantic search?** It can match related meaning even when the wording differs.

</details>

[Next: Step 5, RAG answer with citations](09-rag-answer-with-citations.md)
