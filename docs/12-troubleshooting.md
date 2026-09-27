# Troubleshooting

Use the error or symptom to locate the likely cause. These checks reflect the code and package output from this repository.

| Error message or symptom | Cause | Fix |
|---|---|---|
| `model_decommissioned` or a model request returns 404 | The Groq model name may no longer be available to the account. | Check Groq's current model list and use an available ID. Step 5 and `app.py` both currently use `qwen/qwen3.8-27b`; the dashboard card that says “Llama 3.3” is only a fixed label. |
| `groq.RateLimitError` or HTTP 429 | The request exceeded the account's rate limit. | The app retries up to three times with 1- and 2-second waits when the error text contains “rate”. The terminal script has no retry. If the limit continues, wait and check the provider's rate-limit dashboard. |
| Pinecone index not found | Step 3 has not created the index, or the name differs. | Create/use `rag-index` and check the Pinecone console. |
| Pinecone dimension mismatch | The index's configured dimension does not match each embedding's length. | The code requests 2,048 dimensions. The NVIDIA model card documents a 2,048-value embedding. Recreate the index with the matching dimension if needed. |
| Missing API key or app reports authentication failure | A key is absent, invalid, or not available to the process. | Check the required environment names or Streamlit secrets. Step 5 currently sets three key variables to empty strings. Step 3 and step 4 contain key assignments in source; replace them with your own secure configuration. |
| Streamlit Cloud cannot read a secret | The key is missing from the app's Secrets setting or has a TOML syntax error. | Add valid TOML key-value pairs in the deployed app's Advanced settings → Secrets. Do not commit the local secrets file. |
| Step 1 prints 0 pages, then `IndexError: list index out of range` | `step1_load.py` scans its parent folder, but the tracked PDFs are in `data/` . | Point the loader at the folder containing the PDFs before using the step. The current code has not been changed. |
| Chat input stays white in dark mode | Streamlit's input styling overrides some of the custom CSS. | Inspect the CSS selectors for `stChatInput` and `stChatInputTextArea` in `app.py` and adjust the override for the installed Streamlit version. |
| Python reports that a module cannot be found | The project interpreter has not installed that dependency, or PyCharm is using another interpreter. | Activate the project virtual environment and run `python -m pip install -r requirements.txt`. |
| `create_sample_docs.py` cannot be opened | The file is absent in this checkout. | Use the three PDFs already in `data/`, or obtain the generator from the video author. |
| Step 2 says 16 chunks but dashboard says 17 | The dashboard has a hard-coded chunk statistic. | Treat step 2's run output as the observed count. The app does not calculate that card from Pinecone. |

Groq lists `qwen/qwen3.8-27b` as a current model in its [model documentation](https://console.groq.com/docs/model/qwen/qwen3.8-27b). Models can change, so check the provider page if an ID stops working.

[Next: Interview questions](13-interview-questions.md)
