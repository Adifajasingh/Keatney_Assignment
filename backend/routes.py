from fastapi import APIRouter
from pathlib import Path
import time
from app.logger import log_search, get_metrics
from app.search.hybrid import HybridSearch

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

bm25_path = BASE_DIR / "data/index/bm25/bm25.pkl"
vector_path = BASE_DIR / "data/index/vector/vector"

search_engine = HybridSearch(bm25_path, str(vector_path))

# simple in-memory metrics
request_count = 0
total_latency = 0
feedback_store = []


@router.get("/health")
def health():
    return {"status": "ok", "message": "Hybrid search API running"}

@router.post("/search")
def search(query: str, top_k: int = 5, alpha: float = 0.5):

    start = time.time()

    results = search_engine.search(query, top_k=top_k, alpha=alpha)

    latency = (time.time() - start) * 1000

    log_search(
        query,
        top_k,
        alpha,
        latency,
        len(results)
    )

    formatted = [
        {"doc_id": doc_id, "score": float(score)}
        for doc_id, score in results
    ]

    return {
        "query": query,
        "latency_ms": latency,
        "results": formatted
    }


@router.get("/metrics")
def metrics():

    metrics = get_metrics()

    return {
        "total_requests": metrics["total_requests"],
        "average_latency_ms": metrics["avg_latency"],
        "top_queries": metrics["top_queries"],
         "zero_result_queries": metrics["zero_result_queries"]
    }

@router.post("/feedback")
def feedback(query: str, doc_id: str, relevant: bool):

    entry = {
        "query": query,
        "doc_id": doc_id,
        "relevant": relevant
    }

    feedback_store.append(entry)

    return {
        "message": "feedback recorded",
        "entry": entry
    }
