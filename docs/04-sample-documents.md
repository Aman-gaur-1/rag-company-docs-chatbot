# Sample company documents

The project indexes three PDFs already stored in `data/`. Together they contain six pages of HR, IT security, and product information.

## The three PDFs

| File | What it contains |
|---|---|
| `ConsoleFlare_HR_Policy.pdf` | Leave, working hours, remote work, conduct, and employee benefits. |
| `ConsoleFlare_IT_Security.pdf` | Passwords, data classification, incident reporting, and acceptable use. |
| `ConsoleFlare_Product_Guide.pdf` | LearnFlow features, plans, customer support, refunds, and data export. |

Each PDF has two pages. Page references shown to learners start at 1, although the loader stores page indexes starting at 0.

## Why these files matter

The answers should come from the text in these PDFs. For example, the HR policy says full-time employees receive 24 paid annual leave days per calendar year. A response should identify the source as `ConsoleFlare_HR_Policy.pdf` and Page 1.

## Generator file mentioned in the video brief

The task brief names `create_sample_docs.py`, but that file is not present in this repository. The three PDFs are already checked in, so the later pipeline steps can read them directly.

### Run it

The requested command was run from the project folder:

```text
C:\Users\Aman\AppData\Local\Programs\Python\Python312\python.exe: can't open file 'C:\\Users\\Aman\\PycharmProjects\\rag_knowledge_assistant\\create_sample_docs.py': [Errno 2] No such file or directory
```

No script output can be shown because the file is missing.

[Next: Step 1, load PDFs](05-load-pdfs.md)
