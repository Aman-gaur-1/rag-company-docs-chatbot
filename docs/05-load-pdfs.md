# Step 1: Load PDFs

This script uses `PyPDFLoader` to turn PDF pages into LangChain documents with page and source metadata.

## Goal

Read PDF files and inspect the first loaded page.

## Why this step exists

A PDF is designed for people to read. The retriever needs text and metadata it can process. `PyPDFLoader` creates one document per page and records where that page came from.

For example, if the HR policy is two pages long, the loader should create two page documents. Later steps use the source and page metadata to show citations.

## Full code

{% code title="step1_load.py" lineNumbers="true" %}
```python
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
```
{% endcode %}

## Line-by-line explanation

### Imports and folder path

- `from pathlib import Path` imports Python's path helper.
- `import os` gives access to `os.listdir`, which reads folder contents.
- `from langchain_community.document_loaders import PyPDFLoader` imports the PDF loader.
- `DATA_DIR = Path(__file__).parent` points to the folder containing `step1_load.py`. The PDFs in this checkout are in a subfolder named `data/`, so this path does not point to them.
- `all_documents = []` starts an empty list for the pages.

### Find and load PDFs

The `for` loop sorts the names returned by `os.listdir(DATA_DIR)`. The `if filename.endswith(".pdf")` condition skips non-PDF files. For each PDF it finds, `os.path.join` builds the full path, `PyPDFLoader(filepath)` creates a loader, and `loader.load()` returns one document per page. `extend()` adds those pages to `all_documents`.

The print line reports each filename and its page count. The next print line reports the total documents, which here means PDF pages.

### Preview the first page

- `print("\n ---Preview of first page----")` prints a heading.
- `doc = all_documents[0]` selects the first page. Lists use zero-based positions, so `0` means the first item. This line raises an error if the list is empty.
- The next lines print the source path, the page number plus one, and the first 300 characters of page text.

The loader stores page numbers starting at 0. Adding 1 makes the number shown to a reader match the usual page numbering that starts at 1.

## Run it

~~~bash
python step1_load.py
~~~

### Actual output

This is the real output from the checkout. Ellipses omit unshown traceback lines; every other line below is unchanged.

~~~text
C:\Users\Aman\PycharmProjects\rag_knowledge_assistant\step1_load.py:12: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
...
 Total documents loaded: 0 pages

 ---Preview of first page----
Traceback (most recent call last):
...
IndexError: list index out of range
~~~

The script searches the project root, but the PDFs are under `data/` . It finds no pages, then fails when it tries to select the first one. The notes leave the source file unchanged; this path mismatch needs to be resolved before relying on this step.

## Common mistakes

- Running a script from a different working directory and using a relative path that no longer points to the PDFs.
- Putting the PDFs in `data/` while the script scans its own folder.
- Assuming `all_documents[0]` is safe when no PDF has been loaded.

## Check yourself

<details>
<summary>Answer</summary>

1. **What does the loader return?** A list of page-level `Document` objects.
2. **Why does this run stop?** The configured folder contains no PDFs, so the documents list is empty.
3. **Why does the displayed page use `+ 1`?** The loader stores the first page as index 0.

</details>

[Next: Step 2, chunking](06-chunking.md)
