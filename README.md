# Company Docs AI Chatbot (End-to-End RAG Project)

Watch the full build in Hindi: https://youtu.be/EYJLZFHmP7o

Live demo: https://rag-company-docs-chatbot-nvgkrf9snkgzcze2fx3bmv.streamlit.app/


An AI chatbot that answers questions from company PDFs (HR policy, IT security, product guide) and cites the source file and page for every answer. It replies "I don't know" when the answer isn't in the documents.

**Stack:** LangChain, NVIDIA AI Endpoints (nvidia/nemotron-3-embed-1b), Pinecone, Groq, Streamlit

## Run it
1. `pip install -r requirements.txt`
2. Add NVIDIA_API_KEY, PINECONE_API_KEY, and GROQ_API_KEY to `.streamlit/secrets.toml`
3. `python create_sample_docs.py` then `python step3_embed_store.py`
4. `streamlit run app.py`
