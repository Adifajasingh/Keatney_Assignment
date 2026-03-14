from pathlib import Path

from app.search.bm25 import BM25Index
from app.search.vector import VectorIndex

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DOCS = BASE_DIR / "data" / "processed" / "docs.jsonl"

BM25_PATH = BASE_DIR / "data" / "index" / "bm25" / "bm25.pkl"

VECTOR_PATH = BASE_DIR / "data" / "index" / "vector" / "vector"


def build_bm25():

    print("Building BM25 index...")

    bm25 = BM25Index()
    bm25.build(PROCESSED_DOCS)
    bm25.save(BM25_PATH)

    print("BM25 index saved")


def build_vector():

    print("Building vector index...")

    vector = VectorIndex()
    vector.build(PROCESSED_DOCS)
    vector.save(str(VECTOR_PATH))

    print("Vector index saved")


if __name__ == "__main__":

    build_bm25()
    build_vector()

    print("Indexing complete.")
