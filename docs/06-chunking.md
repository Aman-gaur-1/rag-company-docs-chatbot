# Step 2: Chunking

The script loads the PDFs from `data/` and splits their pages into overlapping text chunks. Chunking gives search smaller passages to compare with a question.

## Goal

Split PDF page text into chunks of about 1,000 characters, with 200 characters shared between neighboring chunks.

## Why this step exists

A long page may contain several topics. If the app searches the whole page as one unit, useful details can be mixed with unrelated text. Smaller chunks make it easier to retrieve the passage that answers a question.

Overlap keeps a little text from the end of one chunk at the start of the next. For example, with a 10-character chunk and 2-character overlap:

~~~text
Chunk 1: ABCDEFGHIJ
Chunk 2:         IJKLMNOPQR
                 `` shared text
~~~

Here the script uses 1,000 characters and 200 characters of overlap. A chunk is text, not a token count.

## Full code

{% code title="step2_chunk.py" lineNumbers="true" %}
```python
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
```
{% endcode %}

## Line-by-line explanation

### Imports and settings

- `import os` is used to list files and print each chunk's source filename.
- `PyPDFLoader` reads each PDF page.
- `RecursiveCharacterTextSplitter` splits long text at a sequence of boundaries.
- `Path` builds the path to the data directory.
- `DATA_DIR` points to the `data/` folder beside the script.
- `CHUNK_SIZE = 1000` sets the target chunk length in characters.
- `CHUNK_OVERLAP = 200` sets how much text is repeated between neighboring chunks.

### Load the pages

As in step 1, the loop sorts filenames, selects PDFs, loads their pages, and extends `all_documents`. Unlike step 1, this file points to `Path(__file__).parent/'data'`, which matches the folder in this checkout. The print statement shows how many pages were loaded and where from.

### Split and preview

The splitter tries these boundaries in order: blank line, newline, period, space, and finally any character. This helps keep chunks near natural boundaries when possible. `split_documents(all_documents)` returns chunk documents with metadata carried forward.

The script prints the chunk count and settings. The final loop shows at most three chunks. `os.path.basename` removes folder names from the source for display; the page number adds 1 to the zero-based metadata index; `len(chunk.page_content)` counts characters. The content preview is limited to 200 characters.

## Run it

~~~bash
python step2_chunk.py
~~~

### Actual output

This is the real output. The loader warning and the three preview lines are from the terminal run.

~~~text
C:\Users\Aman\PycharmProjects\rag_knowledge_assistant\step2_chunk.py:13: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
Loaded 6  Pages from C:\Users\Aman\PycharmProjects\rag_knowledge_assistant\data

Split into 16 chunks (size=1000, overlap=200 

----Chunk 1 | ConsoleFlare_HR_Policy.pdf, Page 1 | 927 chars---
ConsoleFlare  |  HR Policy Manual v3.2
HR Policy Manual
Version 3.2  |  Effective January 2025
1. Leave Policy
All full-time employees at ConsoleFlare are eligible for the following leave benefits:
An...

----Chunk 2 | ConsoleFlare_HR_Policy.pdf, Page 1 | 985 chars---
Bereavement Leave: Up to 5 days of paid leave for the death of an immediate family member (spouse,
parent, child, or sibling).
To apply for leave, submit a request through the HR portal at least 3 wor...

----Chunk 3 | ConsoleFlare_HR_Policy.pdf, Page 1 | 387 chars---
their probation period (6 months). A remote work agreement must be signed and approved by the department
head. Employees must maintain a stable internet connection and be available during core hours.
...
~~~

The run found 6 pages and created 16 chunks. The dashboard currently displays 17 chunks as a fixed statistic; that number does not match this run.

## Common mistakes

- Using the project root instead of the `data/` folder.
- Setting overlap to a value larger than the chunk size.
- Treating character counts as token counts. The code measures characters.

## Check yourself

<details>
<summary>Answer</summary>

1. **Why use overlap?** It keeps context that might otherwise fall across a chunk boundary.
2. **How large is the overlap here?** 200 characters.
3. **How many chunks did this run create?** 16.

</details>

[Next: Step 3, embeddings and Vector Store](07-embeddings-and-vector-store.md)
