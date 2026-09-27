# Why RAG?

Learn why a chatbot needs to retrieve private company information before answering, and how this project uses that idea.

## Why a company chatbot needs help

A general language model does not automatically know what is inside a company's HR policy, IT guide, or product manual. If asked about those files without being given their contents, it may guess. That answer can sound confident and still be wrong.

## The RAG idea

RAG means retrieval-augmented generation. Before the model writes an answer, the app searches a collection of company text and gives the most relevant pieces to the model as context.

Think of an open-book exam. The student first finds the right page, then writes an answer from it. In this project, the retriever finds text from the PDFs and the language model turns that text into a response with a source.

RAG can ground an answer in supplied documents and reduce unsupported guesses. It does not guarantee that every answer is correct: retrieval can miss useful text, and the model can still misread what it receives.

## Why companies use it

Company policies and product details change. A RAG app can search the current documents at question time, instead of requiring the model to memorize them during training. Access controls and document quality still matter.

## Why this is an interview project

This small project brings together document loading, chunking, embeddings, vector search, prompts, citations, API keys, and deployment. These are job-relevant GenAI skills, and interviewers can ask how each part affects the final answer.

## Where this fits in the Agentic AI series

This project is a RAG chatbot, not an agent. It follows a fixed path: retrieve relevant text, then answer. An agent chooses which tools to use for a task. A retriever like this one can become one of those tools.

[Next: How the project works](02-architecture.md)
