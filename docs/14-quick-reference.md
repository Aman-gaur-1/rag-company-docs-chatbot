# Quick reference

Use this page to remember the run order, commands, project settings, and RAG terms.

## Run order

| Order | File | What it does |
|---:|---|---|
| 1 | `step1_load.py` | Loads pages, but currently points at the wrong directory and fails. |
| 2 | `step2_chunk.py` | Loads the PDFs in `data/` and creates chunks. |
| 3 | `step3_embed_store.py` | Deletes and rebuilds the Pinecone index, then embeds and stores chunks. |
| 4 | `step4_retrieve.py` | Searches for the three most similar chunks. |
| 5 | `step5_rag_answer.py` | Retrieves chunks and asks Groq to answer with citations. |
| App | `app.py` | Runs the Streamlit chat interface after the index and secrets are ready. |

The video brief also names `create_sample_docs.py`, but it is not in this repository. The supplied PDFs are already in `data/`.

## Commands

Activate the virtual environment and install packages:

~~~bash
python -m pip install -r requirements.txt
~~~

Run the local pipeline:

~~~bash
python step1_load.py
python step2_chunk.py
python step3_embed_store.py
python step4_retrieve.py
python step5_rag_answer.py
~~~

Start the app:

~~~bash
streamlit run app.py
~~~

Step 1 currently fails because its data path is wrong. Steps 3 to 5 and the app need valid API credentials and a Pinecone index. Step 3 deletes an existing index before rebuilding it.

## Settings and model names

| Setting | File | Value |
|---|---|---|
| Data folder | `step1_load.py` | Script's parent directory; mismatch because the PDFs are inside `data/` |
| Data folder | `step2_chunk.py`, `step3_embed_store.py` | `data/` beside the script |
| Chunk size | `step2_chunk.py`, `step3_embed_store.py` | 1,000 characters |
| Chunk overlap | `step2_chunk.py`, `step3_embed_store.py` | 200 characters |
| Pinecone index | Steps 3–5, `app.py` | `rag-index` |
| Vector dimension | `step3_embed_store.py` | 2,048 |
| Similarity metric | `step3_embed_store.py` | `cosine` |
| Pinecone serverless location | `step3_embed_store.py` | AWS, `us-east-1` |
| Retrieved chunks | `step4_retrieve.py`, `step5_rag_answer.py` | 3 |
| Retrieved chunks | `app.py` | Slider from 1 to 10, default 3 |
| Embedding model | Steps 3–5, `app.py` | `nvidia/nemotron-3-embed-1b` |
| Truncation setting | Steps 5, `app.py` | `truncate="END"` |
| Truncation setting | Steps 3–4 | Source spells it `trucate="END"` |
| Groq model | `step5_rag_answer.py`, `app.py` | `qwen/qwen3.8-27b` |
| Temperature | `step5_rag_answer.py`, `app.py` | 0.2 |
| Groq retry | `app.py` | Up to 3 tries; wait 1 second, then 2 seconds |
| Dashboard chunk count | `app.py` | Fixed display of 17; step 2 created 16 in the observed run |
| Dashboard LLM label | `app.py` | Fixed “Llama 3.3”; the configured model is Qwen |
| Terminal search question | `step4_retrieve.py`, `step5_rag_answer.py` | “What is the employee leave policy?” |
| Extra terminal questions | `step5_rag_answer.py` | Refund policy; security incident reporting; salary structure |
| Theme color variables | `app.py` | `BG`, `CARD_BG`, `CARD_BG2`, `BORDER`, `TEXT_PRIMARY`, `TEXT_SECONDARY`, `ACCENT`, `ACCENT2`, `ACCENT_DIM`, `ACCENT2_DIM`, `INPUT_BG`, `TAG_BG`, `SHADOW`, `SHADOW2`, `USER_MSG_BG`, `BOT_MSG_BG`, `SIDEBAR_BG`, `BTN_BG`, `BTN_BORDER`, `BTN_HOVER_BG` |
| App controls and lists | `app.py` | Top-k slider: min 1, max 10, default 3; three sample questions; five pipeline labels and five technology tags |

## Glossary

| Term | Meaning |
|---|---|
| **RAG** | Retrieval-augmented generation: search for relevant text, then give it to a model to answer. |
| **Chunk** | A smaller piece of a source document. |
| **Embedding** | A numeric representation of text used to compare meaning. |
| **Vector Store** | A system that stores embeddings and searches for similar vectors. |
| **Top-k** | The number of search results returned. |
| **Retriever** | The part that searches the Vector Store for relevant chunks. |
| **LLM** | Large language model, which generates the answer from the prompt. |
| **Prompt** | The instructions and context sent to the LLM. |
| **Citation** | A reference to the source file and page for a fact. |
| **Hallucination** | An answer that sounds plausible but is unsupported or incorrect. |

[Next: Company Docs Chatbot](README.md)
