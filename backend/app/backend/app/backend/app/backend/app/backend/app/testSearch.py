from pathlib import Path
from app.search.hybrid import HybridSearch

BASE = Path(__file__).resolve().parent.parent.parent

bm25_path = BASE / "data/index/bm25/bm25.pkl"
vector_path = BASE / "data/index/vector/vector"

search = HybridSearch(bm25_path, str(vector_path))

results = search.search("machine learning algorithms", top_k=5)

print(results)
