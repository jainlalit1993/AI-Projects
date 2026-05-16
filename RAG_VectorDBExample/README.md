# RAG and Vector Database Demo

A hands-on Python project that teaches Retrieval-Augmented Generation (RAG) step by step using OpenAI embeddings, a local ChromaDB vector database, and a small set of sample documents.

This repository is designed for learning, demos, workshops, and classroom use. Each script builds on the previous one so you can see how raw embeddings become retrieval, and how retrieval becomes grounded answers.

## What This Project Covers

By working through the scripts in order, you will learn:

- What an embedding is and what it looks like as raw numbers
- How semantically similar text ends up close together in vector space
- How ChromaDB stores vectors, text, and metadata
- How to inspect and visualize embedding clusters
- How similarity search works without keyword matching
- How a full RAG pipeline retrieves context and uses it to ground a chat model response

## Repository Structure

```text
RAG_VectorDBExample/
|-- .env.example
|-- 01_what_is_embedding.py
|-- 02_store_in_vectordb.py
|-- 03_inspect_vectordb.py
|-- 04_visualize_embeddings.py
|-- 05_query_and_retrieve.py
|-- 06_full_rag_pipeline.py
|-- README.md
|-- GIT_GUIDE.md
|-- requirements.txt
`-- data/
    `-- sample_documents.py
```

Generated files created while running the demo:

- `chroma_db/` - local ChromaDB data directory created by script 02
- `embedding_clusters.png` - saved by script 04

## Prerequisites

You will need:

- Python 3.10 or later
- An OpenAI API key in a local `.env` file
- Internet access for OpenAI API calls
- A terminal or IDE that can run Python scripts

Optional but useful:

- DB Browser for SQLite to inspect `chroma_db/chroma.sqlite3`
- VS Code or another editor with Python support

## Setup

### 1. Install dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs the packages used by the demo, including:

- `openai`
- `chromadb`
- `python-dotenv`
- `matplotlib`
- `scikit-learn`
- `numpy`
- `pandas`

### 2. Create your `.env` file

Copy `.env.example` to `.env` and add your API key:

```env
OPENAI_API_KEY=sk-your-key-here
```

Important notes:

- Do not commit `.env`
- The scripts currently use `text-embedding-ada-002` for embeddings
- The RAG script currently uses `gpt-4.1-mini` for chat completions

### 3. Choose a Python command that works on your machine

Depending on your environment, one of these may be correct:

```bash
python 01_what_is_embedding.py
python3 01_what_is_embedding.py
py 01_what_is_embedding.py
```

On Windows, if `python` is not on your PATH, use the full interpreter path or select the Python interpreter in your IDE.

## Run Order

Run the scripts in this order:

```bash
python 01_what_is_embedding.py
python 02_store_in_vectordb.py
python 03_inspect_vectordb.py
python 04_visualize_embeddings.py
python 05_query_and_retrieve.py
python 06_full_rag_pipeline.py
```

Important:

- Script 02 creates and repopulates the vector database
- Scripts 03 to 06 depend on data already being stored in `chroma_db/`
- If you change the sample documents, rerun script 02 before querying or visualizing

## Script Guide

### 01 - What Is an Embedding?

File: `01_what_is_embedding.py`

What it does:

- Calls the embedding model for a sentence
- Prints the vector length and sample values
- Compares sentence pairs using cosine similarity
- Shows that similar meaning leads to higher similarity scores

What you should notice:

- The embedding is a long list of floating-point numbers
- Similar sentences score higher than unrelated ones
- The demo uses cosine similarity computed directly in Python

### 02 - Store Documents in the Vector Database

File: `02_store_in_vectordb.py`

What it does:

- Loads the sample documents from `data/sample_documents.py`
- Generates embeddings for each document
- Stores IDs, embeddings, original text, and metadata in ChromaDB
- Resets the collection each time so the demo starts clean

What you should notice:

- A `chroma_db/` folder appears in the project
- The collection name is `rag_demo`
- Metadata such as title, category, source, and year is stored with each document

### 03 - Inspect the Vector Database

File: `03_inspect_vectordb.py`

What it does:

- Reads the stored collection from ChromaDB
- Prints all document IDs and metadata
- Shows one full embedding vector
- Compares vectors side by side
- Prints a small similarity matrix across categories

What you should notice:

- ChromaDB stores more than just vectors
- Similarity is highest on the diagonal because a document is identical to itself
- Cross-topic similarity is lower than same-topic similarity

### 04 - Visualize Embeddings in 2D

File: `04_visualize_embeddings.py`

What it does:

- Loads all stored embeddings
- Uses PCA to reduce them from 1536 dimensions to 2 dimensions
- Displays a matplotlib figure with category-colored clusters
- Saves the plot as `embedding_clusters.png`

What you should notice:

- Documents from the same category tend to cluster together
- PCA is only a projection, but the structure is still visible
- The saved PNG gives you a persistent artifact for slides or demos

### 05 - Query and Retrieve

File: `05_query_and_retrieve.py`

What it does:

- Embeds a question
- Searches the vector database for the nearest documents
- Prints the top matches with distances, derived similarity scores, and snippets
- Includes demo queries plus an interactive prompt

What you should notice:

- Retrieval is based on vector proximity, not exact keyword matching
- Related phrasing can still find the right document
- The top results usually align with semantic meaning rather than wording

### 06 - Full RAG Pipeline

File: `06_full_rag_pipeline.py`

What it does:

- Retrieves relevant document chunks from ChromaDB
- Builds a grounded prompt using those retrieved documents
- Compares an answer without retrieval to an answer with retrieval
- Includes a short demo set followed by optional interactive mode

What you should notice:

- The no-RAG answer uses general model knowledge
- The RAG answer is constrained to the retrieved context
- The script now handles non-interactive environments safely and will skip input prompts instead of crashing with `EOFError`

## Sample Data

The sample dataset contains 20 short documents across 4 categories:

- Space
- Animals
- Cooking
- Technology

Each document includes:

- `id`
- `text`
- `metadata.title`
- `metadata.category`
- `metadata.source`
- `metadata.year`

This makes the demo useful for:

- obvious retrieval examples
- visible clustering in PCA
- metadata inspection
- classroom discussion across clearly separated topics

Important note:

- The sample `source` and `year` values are illustrative metadata for the demo and should not be treated as formal citations

## ChromaDB Storage

After running script 02, you should see something like:

```text
chroma_db/
|-- chroma.sqlite3
`-- <uuid>/
    |-- data_level0.bin
    |-- header.bin
    |-- length.bin
    `-- link_lists.bin
```

What these files mean at a high level:

- `chroma.sqlite3` stores collection metadata and document records
- the binary files store the vector index used for fast nearest-neighbor lookup

If you want to inspect the database manually:

1. Install DB Browser for SQLite.
2. Open `chroma_db/chroma.sqlite3`.
3. Browse the tables to inspect stored text and metadata.

## Common Issues and Fixes

### `OPENAI_API_KEY` missing or invalid

Symptom:

- authentication errors
- permission errors
- model access errors

Fix:

- confirm `.env` exists in the project root
- confirm the key is valid
- confirm the account or project has access to the models used in the scripts

### `collection not found` or empty retrieval results

Symptom:

- scripts 03 to 06 have nothing meaningful to inspect or retrieve

Fix:

- run `02_store_in_vectordb.py` first
- rerun script 02 after changing the sample data

### `python` command not found

Symptom:

- the shell says `python` is not recognized

Fix:

- try `python3` or `py`
- select the correct interpreter in VS Code
- use the full path to the installed Python executable if needed

### Script 06 stops or exits around an input prompt

Symptom:

- the script behaves differently in an IDE task runner, notebook-like console, or non-interactive shell

Fix:

- the current version skips prompts automatically in non-interactive environments
- if you want the pause-and-continue behavior, run the script in a normal terminal window

### Garbled characters in terminal output

Symptom:

- arrows, separators, or check marks display incorrectly on some Windows terminals

Fix:

- the scripts already call `sys.stdout.reconfigure(encoding="utf-8")`
- if your terminal still looks odd, try Windows Terminal, PowerShell, or VS Code's integrated terminal with UTF-8 support

## Customizing the Demo

To replace the sample data, edit `data/sample_documents.py` and keep the same structure:

```python
{
    "id": "unique_id",
    "text": "Your document text here.",
    "metadata": {
        "title": "Document title",
        "category": "Custom category",
        "source": "Your source label",
        "year": 2024,
    },
}
```

After editing the documents:

1. Run script 02 again to rebuild the ChromaDB collection.
2. Rerun scripts 03 to 06 as needed.

Good extension ideas:

- add more categories
- make the documents longer and split them into chunks
- filter by metadata during retrieval
- compare retrieval quality with different values of `TOP_K`
- swap in your own course notes, policies, or product docs

## Teaching Notes

This repo works well for a classroom or workshop because each script introduces one new concept:

- script 01 explains embeddings
- script 02 introduces storage
- script 03 makes the database visible
- script 04 makes the geometry visible
- script 05 demonstrates retrieval
- script 06 demonstrates grounded generation

Suggested teaching flow:

1. Start with script 01 to demystify embeddings.
2. Run script 02 and show that vectors are stored locally.
3. Use script 03 to inspect the stored records.
4. Use script 04 for the visual payoff.
5. Let students ask their own retrieval questions in script 05.
6. End with script 06 to compare answers with and without RAG.

## Related Files

- `GIT_GUIDE.md` - practical Git installation and workflow notes for beginners
- `data/sample_documents.py` - the demo dataset
- `requirements.txt` - Python dependencies for the project

## Summary

This project demonstrates the complete learning path from embedding generation to retrieval and grounded answers. It is intentionally small enough to understand end to end, while still showing the core ideas behind modern RAG systems:

- embeddings turn meaning into vectors
- vector databases store and search those vectors
- retrieval finds relevant context
- grounded prompts help language models answer using your data instead of relying only on their training
