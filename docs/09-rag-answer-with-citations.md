# Step 5: RAG answer with citations

This script retrieves three chunks, adds their source labels to a prompt, and asks Groq to answer using that context.

## Goal

Combine retrieval and text generation, then print an answer and the sources that were retrieved.

## Why this step exists

Search results are useful to the application, but they are not yet a conversational answer. The prompt asks the LLM to read the matching chunks, answer from those chunks, and cite the source file and page.

The prompt also includes a fallback: if the context does not contain the answer, respond with “I don't know based on the available documents.” This reduces unsupported answers, but a prompt alone cannot guarantee perfect grounding.

## Full code

{% code title="step5_rag_answer.py" lineNumbers="true" %}
```python
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
```
{% endcode %}

## Line-by-line explanation

### Imports, keys, and settings

- `os` provides `os.path.basename` for short source names.
- `NVIDIAEmbeddings` makes question vectors; `PineconeVectorStore` searches the index; `ChatGroq` calls the Groq chat model.
- The script sets `NVIDIA_API_KEY`, `PINECONE_API_KEY`, and `GROQ_API_KEY` to empty strings. This overwrites any values already in those environment variables.
- `INDEX_NAME` is `rag-index`; `TOP_K` is 3.
- The embedding model is `nvidia/nemotron-3-embed-1b`, with `truncate="END"`.
- `ChatGroq` uses `qwen/qwen3.8-27b` and `temperature=0.2`. Temperature controls response variation: lower values usually make answers more consistent.

### Format source text

`format_doc(docs)` loops through retrieved documents, gets the base filename, and converts the zero-based page index to a reader-facing page number by adding 1. It prefixes each chunk with the filename and page, then joins the chunks with a separator.

There is a formatting typo in this function: the source string opens a citation bracket but does not close it before the newline. The Streamlit app's `format_docs` has a closing bracket. The terminal file is documented as written.

### Retrieve and build the prompt

The fixed question is `What is the employee leave policy?`. `similarity_search` returns the three closest chunks. `format_doc` turns them into context for the prompt.

The prompt rules, one by one:

1. Use only the supplied context.
2. If the answer is absent, use the “I don't know” fallback. The quote in the source prompt is missing its closing quotation mark.
3. Keep the answer clear and concise.
4. Cite source documents and page numbers for facts.

`llm.invoke(prompt)` sends the prompt to Groq. The next print displays the answer.

### Print sources and test more questions

The first source loop prints every retrieved filename and page. The `more_questions` list includes refund policy, security incident reporting, and salary structure. Salary is not covered in the supplied PDFs, so it tests the fallback instruction.

For each additional question, the script repeats search, context formatting, prompt creation, and model invocation, then prints the answer and a divider. There is no retry logic in this terminal script.

## Run it

~~~bash
python step5_rag_answer.py
~~~

### Expected output

The terminal prints the connection and question, then a model-generated answer and the retrieved sources. It repeats an answer block for each question in `more_questions`. The exact answer text depends on the API response, so it is not shown here.

~~~text
Connected to Pinecone index 'rag-index'
Question: What is the employee leave policy?
Answer: <model response>
----Source----
1. <filename>, Page <page>
Question: What is the refund policy?
Answer: <model response>
...
Question: What is the salary structure?
Answer: I don't know based on the available documents.
~~~

<!-- TODO: paste real output from the video -->

No API-backed run was performed.

## Common mistakes

- The script's empty key assignments replace credentials set in the shell.
- The index does not exist or was created with a different model dimension.
- The citation label is malformed because the opening bracket is not closed.
- The LLM may not follow the fallback instruction every time; test with questions outside the PDFs.

## Check yourself

<details>
<summary>Answer</summary>

1. **What does the prompt do?** It gives the retrieved text and tells the LLM how to answer from it.
2. **Why is the page number incremented?** PDF metadata counts from zero; readers count from one.
3. **What does the salary question test?** The prompt's out-of-scope fallback.

</details>

[Next: Streamlit web app](10-streamlit-app.md)
