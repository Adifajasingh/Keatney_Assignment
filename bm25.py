import json
import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self):
        self.corpus = []
        self.doc_ids = []
        self.bm25 = None

    def build(self, docs_jsonl):
        with open(docs_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                doc = json.loads(line)
                tokens = doc["text"].lower().split()
                self.corpus.append(tokens)
                self.doc_ids.append(doc["doc_id"])

        self.bm25 = BM25Okapi(self.corpus)

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump({
                "bm25": self.bm25,
                "doc_ids": self.doc_ids,
                "corpus": self.corpus
            }, f)

    def load(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)

        self.bm25 = data["bm25"]
        self.doc_ids = data["doc_ids"]
        self.corpus = data["corpus"]

    def query(self, query, top_k=5):
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.doc_ids, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return ranked
