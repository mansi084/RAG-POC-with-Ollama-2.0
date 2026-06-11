# RAG POC with Ollama

> Ask questions from your own documents — privately, freely, and fully offline.

No ChatGPT. No API keys. No data leaving your machine.
Just upload a document, ask a question, get an answer.

---

## What is this?

A **Proof of Concept** for a **RAG (Retrieval Augmented Generation)** system that:

1. Takes your documents (PDF, TXT, DOCX)
2. Splits them into chunks
3. Converts chunks into vectors (embeddings)
4. Stores vectors locally in ChromaDB
5. Also queries a local SQLite employee database
6. Routes your question to the right source intelligently
7. Falls back to other source if first source fails
8. Combines answers from multiple sources
9. Returns the most accurate answer

---

## Architecture

### TRAINING FLOW:
Your Document
↓
Document Loader (PDF / TXT / DOCX)
↓
Text Splitter (chunks of 500 chars)
↓
nomic-embed-text (converts to vectors)
↓
ChromaDB (saves vectors locally)


### QUERY FLOW:

User asks a Question
  ↓
Query Router (decides which source to use)
  ↓            
Document Source   OR    Database Source    OR       Both
(ChromaDB)                 (SQLite)
  ↓
Answer found? → Reranker → Final Answer 
  ↓
Not found? → Fallback → try other source
  ↓
Still not found? → "No information found"

---

## Project Structure

project/
│
├── config.yaml                    → all settings
├── app.py                         → FastAPI endpoints
├── rag_service.py                 → core RAG brain
├── setup_database.py              → loads CSV into SQLite
├── requirements.txt               → all dependencies
├── .gitignore
│
├── factories/
│   ├── embedding_factory.py       → picks embedding model
│   ├── llm_factory.py             → picks LLM
│   └── vectorstore_factory.py     → picks vector DB
│
├── loaders/
│   └── document_loader.py         → reads PDF/TXT/DOCX
│
├── sources/
│   ├── document_source.py         → handles ChromaDB queries
│   └── database_source.py         → handles SQLite queries
│
├── router/
│   └── query_router.py            → decides which source to use
│
├── reranker/
│   └── reranker.py                → combines best answers
│
├── documents/                     → drop your files here
├── my_database/                   → ChromaDB saves here
└── my_db.sqlite                   → SQLite employee database

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.11** | Core language |
| **Ollama** | Runs AI models locally |
| **Llama3** | LLM that reads and answers |
| **nomic-embed-text** | Converts text to vectors |
| **ChromaDB** | Stores and searches vectors |
| **SQLite** | Local employee database |
| **LangChain** | Connects all components |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |

---

## Prerequisites

- Python 3.10 or higher
- Ollama installed → [Download here](https://ollama.com)
- Git installed
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

---

## Dataset

This project uses a sample of the IBM HR Analytics Employee 
Attrition Dataset for testing purposes.

- **Sample included** → `WA_Fn-UseC_-HR-Employee-Attrition.csv`
- **Full dataset** → [Download from Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

To setup the database run:
```bash
python setup_database.py
```

---

## Setup & Installation

### Step 1 — Clone the repository
```bash
git clone https://github.com/mansi084/RAG-POC-with-Ollama-2.0
cd RAG-POC-with-Ollama-2.0
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Pull Ollama models
```bash
# Pull the LLM
ollama pull llama3

# Pull the embedding model
ollama pull nomic-embed-text
```
### Step 5 — Setup SQLite database
```bash
# Place the CSV file in the project folder first
python setup_database.py
```

### Step 6 — Start the server
```bash
uvicorn app:app --reload
```

### Step 7 — Open API docs
http://127.0.0.1:8000/docs

---

## API Endpoints

### Upload a Document
```json
POST /upload
```
Response:
```json
{
  "message": "Successfully trained on 12 chunks!"
}
```

---

### Ask a Question
```json
POST /ask
{
  "question": "What is the leave policy?"
}
```
Response:
```json
{
  "answer": "According to the policy, every employee gets 20 paid leaves per year."
}
```

---

## How Routing Works

| Question type | Routed to |
|---|---|
| "What is the leave policy?" | Documents (ChromaDB) |
| "How many employees are in Sales?" | Database (SQLite) |
| "Does the salary match the policy?" | Both sources |

---

## Configuration

Everything is controlled from `config.yaml`:

```yaml
llm:
  provider: ollama
  model: llama3          

embedding:
  provider: ollama
  model: nomic-embed-text

vectorstore:
  provider: chroma
  path: ./my_database

chunking:
  chunk_size: 500
  chunk_overlap: 50

database:
  provider: sqlite
  path: ./my_db.sqlite
```
--- 

## Features

- 100% local — no internet needed
- Free — no API costs
- Private — data never leaves your PC
- Pluggable — swap models via config
- Smart routing — questions go to right source
- Multi-source — answers from documents AND database
- Reranker — combines best answers
- Semantic search — finds meaning not just keywords
- Online training — upload new docs instantly
- Supports PDF, TXT, DOCX
- REST API powered by FastAPI
- Auto-generated API docs at `/docs`

---

##  Supported File Types

PDF
Word Document
Plain Text 

---

## Privacy

-  All processing happens on your machine
-  No data sent to any external server
-  Works completely offline
-  Your documents never leave your PC

---










