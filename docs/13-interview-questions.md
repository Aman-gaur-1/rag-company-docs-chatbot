# Interview questions

Use these questions to explain design choices and debug the exact project.

## Concepts

<details>
<summary>Why split documents into chunks?</summary>

Search can return a focused passage instead of an entire long page. This project targets 1,000 characters per chunk with 200 characters of overlap.

</details>

<details>
<summary>Why use overlap?</summary>

A fact may sit near a chunk boundary. Repeating some text in the next chunk can preserve enough context for retrieval.

</details>

<details>
<summary>What is an embedding?</summary>

It is a list of numbers that represents text for similarity search. Here NVIDIA's model creates a 2,048-dimensional vector for each passage.

</details>

<details>
<summary>What does top-k mean?</summary>

It is how many search results to return. The terminal RAG script starts with k=3, while the app lets the user choose from 1 to 10.

</details>

<details>
<summary>How is RAG different from fine-tuning?</summary>

RAG retrieves external text at question time and includes it in the prompt. Fine-tuning changes model behavior through training on examples; it is not how this project updates company documents.

</details>

## Design and debugging

<details>
<summary>Why does the prompt say to answer only from context?</summary>

It directs the model to use retrieved passages instead of relying on unrelated knowledge. The prompt also asks for a fallback when the answer is absent. These rules help reduce unsupported answers but do not prove an answer is correct.

</details>

<details>
<summary>How would you reduce hallucination further?</summary>

Check that retrieval returns the right pages, improve chunk boundaries, keep source labels in the context, and evaluate answers against questions with known answers. You can also validate whether every factual sentence cites a retrieved source.

</details>

<details>
<summary>How would you add new documents without rebuilding everything?</summary>

Load and chunk only the new files, embed those chunks, and upsert them with stable IDs and source metadata. The current step 3 deletes and recreates the entire index, so its ingestion flow would need to change first.

</details>

<details>
<summary>How would you evaluate answer quality?</summary>

Prepare questions with expected answers and source pages. Measure whether the correct chunks were retrieved, whether answers match those sources, and whether out-of-scope questions receive the fallback.

</details>

<details>
<summary>Why must the Pinecone dimension match the embedding model?</summary>

Pinecone stores vectors with a fixed number of values per index. The current index uses 2,048 because the selected NVIDIA model outputs vectors of that length.

</details>

<details>
<summary>Why keep source and page metadata?</summary>

The answer prompt needs to identify where each passage came from. The loader records a zero-based page index; the code adds 1 for the page number shown to people.

</details>

<details>
<summary>How would you turn this into an agent?</summary>

Make retrieval one available tool and let an agent decide whether to call it or another tool for a question. This chatbot currently follows a fixed retrieve-then-answer sequence.

</details>

<details>
<summary>What would you change before production?</summary>

Move credentials out of the Python files, use stable chunk IDs, avoid deleting the index on every ingestion, add access controls, and evaluate retrieval and answer quality. The current repository is a learning example and has known issues listed in the troubleshooting page.

</details>

[Next: Quick reference](14-quick-reference.md)
