# GitHub and Streamlit Cloud deployment

Put the app and its dependencies in GitHub, configure secrets in Streamlit Community Cloud, and deploy the `app.py` entrypoint.

## Goal

Make the Company Docs Chatbot accessible from a public Streamlit URL without committing API keys.

## 1. Keep credentials out of Git

For local development, store keys in `.streamlit/secrets.toml`. The file belongs on your machine and is already listed in `.gitignore`. Do not add real secrets to source files.

For the deployed app, paste the same TOML key-value entries into **Advanced settings → Secrets** during deployment. Streamlit makes them available through `st.secrets`.

## 2. Read the ignore rules

| Entry in `.gitignore` | Purpose |
|---|---|
| `.streamlit/secrets.toml` | Keeps local Streamlit API keys out of commits. |
| `.streamlit/secrets.toml.py` | Ignores a Python file with a similar name. |
| `__pycache__/`, `*.pyc`, `*.pyo` | Excludes Python cache files. |
| `venv/`, `.venv/`, `.env/` | Excludes virtual environment directories. A plain file named `.env` is not covered by `.env/` in this file. |
| `.idea/`, `.vscode/`, `*.swp` | Excludes IDE files and swap files. |
| `.DS_Store`, `Thumbs.db` | Excludes operating-system metadata. |
| `company_docs/` | Excludes that folder; the current sample PDFs under `data/` remain tracked. |

Before each commit, check `git status` and stage specific project files. Do not use `git add .` until you have confirmed it cannot include credentials.

## 3. Initialize and commit

If you copied the project into a folder that is not already a Git repository, use:

~~~bash
git init
git status
git add app.py requirements.txt .gitignore data step1_load.py step2_chunk.py step3_embed_store.py step4_retrieve.py step5_rag_answer.py
git status
git commit -m "Add Company Docs Chatbot"
~~~

This checkout already has a Git repository, so do not run `git init` inside it. Review the staged file list before committing.

## 4. Create the GitHub repository

Create an empty repository on GitHub and copy its HTTPS URL.

## 5. Push to GitHub

Connect the local repository and push the commit:

~~~bash
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git branch -M main
git push -u origin main
~~~

If Git prompts for a password over HTTPS, use a GitHub Personal Access Token with the needed repository permissions instead of your account password. Treat the token like an API key: never paste it into source code or notes.

## 6. Connect the app to Streamlit Community Cloud

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with the GitHub account that can access the repository.
2. Select **Create app**.
3. Choose the GitHub repository, branch, and entrypoint file: `app.py`.
4. Open **Advanced settings → Secrets** and paste the three key-value entries from your local `secrets.toml`. Do not upload the local file.
5. Select a supported Python version if needed.

See Streamlit's [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [secrets guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) for the current screens.

## 7. Deploy and copy the URL

Click **Deploy**. Wait for the app to finish starting, then copy its Streamlit URL.

## 8. Update the deployed app

Commit and push changes to the connected branch:

~~~bash
git add app.py requirements.txt
git commit -m "Update Company Docs Chatbot"
git push
~~~

Community Cloud watches the connected GitHub branch and redeploys when it detects a push. If requirements change, it also reinstalls dependencies.

## Common mistakes

- Pushing a secrets file or key assignment to GitHub.
- Choosing the wrong branch or entrypoint file.
- Forgetting to add package dependencies to `requirements.txt`.
- Expecting a deployment to work before the Pinecone index exists.

## Check yourself

<details>
<summary>Answer</summary>

1. **Where do deployed secrets go?** Streamlit Community Cloud's Advanced settings → Secrets.
2. **Which file starts the app?** `app.py`.
3. **What makes a later code update deploy?** Pushing a commit to the connected branch.

</details>

[Next: Troubleshooting](12-troubleshooting.md)
