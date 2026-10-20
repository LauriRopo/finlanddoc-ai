# FinlandDoc AI

A lightweight Finnish-language document search application built with Python and Streamlit.

## Features

- Search Finnish text documents using BM25 ranking.
- Upload UTF-8 `.txt` files.
- Search document content with natural-language questions.
- Display relevant text passages.
- Validate empty inputs and oversized files.
- Automated tests with pytest.

## Tech stack

- Python
- Streamlit
- rank-bm25
- pytest

## Getting started

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

Windows CMD:

```bat
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit rank-bm25 pytest
```

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Run tests

```bash
pytest -v
```

## How it works

The application splits document text into sentences and ranks relevant passages using BM25. It returns up to three matching passages.

The current search is lexical rather than semantic. It does not yet use an LLM, embeddings, or a vector database, and it may miss relevant results when Finnish words appear in different grammatical forms.

## Security considerations

- Uploaded text is processed by the application without requiring an external AI API.
- Uploaded files are restricted to `.txt` and a maximum size of 1 MB.
- Environment files and virtual environments should not be committed to Git.

## Future improvements

- Improve Finnish-language tokenization and stemming.
- Add stronger retrieval tests and relevance evaluation.
- Add source-grounded LLM answers.
- Explore hybrid retrieval using BM25 and vector search.

## Project status

Portfolio project under active development.
