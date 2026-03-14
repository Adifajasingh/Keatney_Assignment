# Hybrid Search + KPI Dashboard System

This project implements a **hybrid document search engine** that combines **lexical search (BM25)** with **semantic search (sentence-transformer embeddings + FAISS)**. It exposes a **FastAPI backend** and a **Streamlit dashboard** to search documents, monitor system KPIs, and evaluate retrieval performance.

---

## System Architecture

```
User Query
    ↓
Streamlit Dashboard
    ↓
FastAPI API
    ↓
Hybrid Search Engine
    ├── BM25 Index         (keyword search)
    └── Vector Index       (semantic search via FAISS)
    ↓
SQLite Logging + Metrics
    ↓
Evaluation Harness         (Recall / MRR / nDCG)
```

---

## Features

### Hybrid Retrieval
- BM25 keyword matching
- Sentence-transformer semantic embeddings
- FAISS vector similarity search

### API Backend (FastAPI)
- `/search` — Execute hybrid search queries
- `/metrics` — Retrieve system performance metrics
- `/feedback` — Submit user relevance feedback
- `/health` — System status check

### Observability
- SQLite query logging
- Latency tracking
- Top queries analytics
- Zero-result query detection

### Evaluation Harness
- Recall@10
- MRR@10
- nDCG@10

### Dashboard (Streamlit)
- Search interface
- KPI metrics visualization
- Evaluation results inspection

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| Language | Python |
| API Framework | FastAPI |
| Frontend | Streamlit |
| Vector DB | FAISS |
| Embeddings | Sentence Transformers |
| Lexical Retrieval | Rank-BM25 |
| Database | SQLite |
| Data Processing | Pandas |

---

## Project Structure

```
hybrid-search-dashboard/
├── backend/
│   └── app/
│       ├── api/
│       ├── search/
│       ├── logger.py
│       ├── eval.py
│       ├── index.py
│       ├── ingestion.py
│       └── main.py
├── frontend/
│   └── dashboard.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── index/
│   ├── eval/
│   ├── metrics/
│   └── logs/
├── requirements.txt
├── up.sh
└── README.md
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the System

The system consists of two components: a **FastAPI backend** and a **Streamlit dashboard**.

#### Start the Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

The backend API will be available at:
- **API Base URL:** `http://127.0.0.1:8000`
- **Swagger UI (Docs):** `http://127.0.0.1:8000/docs`

#### Start the Dashboard

Open a separate terminal and run:

```bash
streamlit run frontend/dashboard.py
```

The dashboard will be available at `http://localhost:8501`.

---

## API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health` | `GET` | Check if API is running |
| `/search` | `POST` | Run hybrid search |
| `/metrics` | `GET` | Retrieve system metrics |
| `/feedback` | `POST` | Log user feedback |

---

## Evaluation

Evaluation measures search quality using the following metrics:

- **Recall@10**
- **Mean Reciprocal Rank (MRR@10)**
- **nDCG@10**

### Evaluation Files

The evaluation process relies on the following data files:

```
data/eval/queries.jsonl
data/eval/qrels.json
```

### Run Evaluation

Navigate to the backend directory and run the evaluation module:

```bash
cd backend
python -m app.eval
```

Results will be saved to `data/metrics/experiments.csv` and visualized in the **Evaluation** page of the dashboard.

---

## Observability & Logging

The system logs all search queries to a **SQLite** database. Logged information includes:

- Query text
- Search latency
- Result count
- Top queries
- Zero-result queries

**Database location:** `data/logs/search_logs.db`

---

## Hybrid Search Method

### Lexical Search
BM25 ranking using the `rank-bm25` library.

### Semantic Search
Sentence embeddings generated using `sentence-transformers` and indexed using FAISS.

### Hybrid Scoring

Final ranking score is computed as:

```
hybrid_score = α × normalized_bm25 + (1 - α) × normalized_vector
```

Where **α** controls the balance between lexical and semantic search.

---

## Dashboard Features

The Streamlit dashboard provides:

- Document search interface
- System KPI metrics
- Top query analytics
- Zero-result query tracking
- Evaluation metric visualization

---

## Author

**Aditya Gupta**
