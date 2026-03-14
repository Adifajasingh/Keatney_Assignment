import json
import csv
from pathlib import Path
from datetime import datetime

from app.search.hybrid import HybridSearch

BASE = Path(__file__).resolve().parent.parent.parent

queries_path = BASE / "data/eval/queries.jsonl"
qrels_path = BASE / "data/eval/qrels.json"

bm25_path = BASE / "data/index/bm25/bm25.pkl"
vector_path = BASE / "data/index/vector/vector"

metrics_file = BASE / "data/metrics/experiments.csv"

search_engine = HybridSearch(bm25_path, str(vector_path))


def recall_at_k(results, relevant, k=10):

    retrieved = [doc for doc, _ in results[:k]]

    hits = len(set(retrieved) & set(relevant))

    return hits / len(relevant) if relevant else 0


def mrr_at_k(results, relevant, k=10):

    for rank, (doc, _) in enumerate(results[:k], start=1):
        if doc in relevant:
            return 1 / rank

    return 0


def ndcg_at_k(results, relevant, k=10):

    dcg = 0

    for i, (doc, _) in enumerate(results[:k], start=1):
        if doc in relevant:
            dcg += 1 / (i).bit_length()

    ideal_hits = min(len(relevant), k)

    idcg = sum(1 / (i).bit_length() for i in range(1, ideal_hits + 1))

    return dcg / idcg if idcg > 0 else 0


def run_eval():

    queries = []
    with open(queries_path) as f:
        for line in f:
            queries.append(json.loads(line))

    with open(qrels_path) as f:
        qrels = json.load(f)

    recalls = []
    mrrs = []
    ndcgs = []

    for q in queries:

        qid = q["query_id"]
        query = q["query"]

        results = search_engine.search(query, top_k=10)

        relevant = qrels.get(qid, [])

        recalls.append(recall_at_k(results, relevant))
        mrrs.append(mrr_at_k(results, relevant))
        ndcgs.append(ndcg_at_k(results, relevant))

    avg_recall = sum(recalls) / len(recalls)
    avg_mrr = sum(mrrs) / len(mrrs)
    avg_ndcg = sum(ndcgs) / len(ndcgs)

    Path(BASE / "data/metrics").mkdir(parents=True, exist_ok=True)

    with open(metrics_file, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now().isoformat(),
            avg_recall,
            avg_mrr,
            avg_ndcg
        ])

    print("Evaluation complete")
    print("Recall@10:", avg_recall)
    print("MRR@10:", avg_mrr)
    print("nDCG@10:", avg_ndcg)


if __name__ == "__main__":
    run_eval()
