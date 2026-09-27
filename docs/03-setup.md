# Project setup

Set up Python, install the packages listed in `requirements.txt`, and keep API credentials out of Git.

## Create the project in PyCharm

1. Clone the repository from GitHub, or open the existing project folder in PyCharm.
2. Open **Settings → Project → Python Interpreter**.
3. Choose **Add Interpreter → Add Local Interpreter → Virtualenv**.
4. Create a virtual environment in the project folder and select Python 3.12. The current step 1 file uses f-string syntax that requires Python 3.12.
5. Open PyCharm's terminal. Activate the environment if PyCharm has not done so automatically, then install the dependencies:

{% tabs %}
{% tab title="Windows" %}
```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
```
{% endtab %}
{% tab title="macOS / Linux" %}
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```
{% endtab %}
{% endtabs %}

## What the requirements do

| Package | Why it is here |
|---|---|
| `langchain` | Provides the LangChain framework used to connect pipeline components. |
| `langchain-community` | Supplies `PyPDFLoader`, which reads PDF pages into documents. |
| `langchain-text-splitters` | Supplies `RecursiveCharacterTextSplitter` for making overlapping chunks. |
| `langchain-nvidia-ai-endpoints` | Calls NVIDIA's embedding model. |
| `langchain-groq` | Connects LangChain to the Groq chat model. |
| `langchain-pinecone` | Connects LangChain documents and embeddings to Pinecone. |
| `pinecone-client` | Creates, checks, and deletes Pinecone indexes through the Pinecone API. |
| `pypdf` | Reads PDF content for the LangChain PDF loader. |
| `streamlit` | Builds and runs the web chat app. |

The package file uses minimum version ranges, not exact pins. The environment used for this walkthrough had Python 3.12 and installed the listed requirements successfully.

## Get the three API credentials

Create accounts and API keys from each provider:

1. [NVIDIA API Catalog](https://build.nvidia.com/) provides the embedding endpoint. NVIDIA offers free API access for development; see its [API quickstart](https://docs.api.nvidia.com/nim/docs/api-quickstart).
2. [Pinecone](https://www.pinecone.io/) stores the vectors. Its [Starter plan](https://www.pinecone.io/pricing/) is free for trying the service.
3. [Groq Console](https://console.groq.com/) provides the chat model endpoint. Groq offers a Free plan with provider-set [rate limits](https://console.groq.com/docs/rate-limits).

Free access has provider-set limits and can change. Check the provider dashboard before a long run.

## Where credentials belong

The Streamlit app reads `NVIDIA_API_KEY`, `PINECONE_API_KEY`, and `GROQ_API_KEY` from `st.secrets`, then falls back to environment variables. For local app development, create `.streamlit/secrets.toml`:

```toml
NVIDIA_API_KEY = "your-nvidia-api-key-here"
PINECONE_API_KEY = "your-pinecone-api-key-here"
GROQ_API_KEY = "your-groq-api-key-here"
```

The terminal scripts do not load `secrets.toml`. In the current files, step 3 and step 4 assign key values directly in the Python source, while step 5 assigns empty strings. Do not use those assignments as a credential-management pattern. The keys present in the tracked step 3 and step 4 files have been omitted from the notes for safety. Replace them with your own credentials stored outside source code before running these steps.

{% hint style="danger" %}
Never commit API keys, tokens, or `.streamlit/secrets.toml` to GitHub. If a key has been committed or shared, revoke it and create a new one.
{% endhint %}

## What `.gitignore` excludes

| Pattern | What Git ignores |
|---|---|
| `.streamlit/secrets.toml` | Local Streamlit secrets. |
| `.streamlit/secrets.toml.py` | A similarly named local file; this is not a TOML secrets file. |
| `__pycache__/`, `*.pyc`, `*.pyo` | Python-generated cache files. |
| `venv/`, `.venv/`, `.env/` | Virtual environment folders. |
| `.idea/`, `.vscode/`, `*.swp` | IDE settings and swap files. |
| `.DS_Store`, `Thumbs.db` | Operating-system metadata files. |
| `company_docs/` | A generated-PDF folder. The actual PDFs in this repo are under `data/` and are tracked. |

The current `.gitignore` does not ignore a plain `.env` file. Check `git status` before committing and never stage local credentials.

[Next: Sample company documents](04-sample-documents.md)
