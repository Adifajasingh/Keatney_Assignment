import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


class VectorIndex:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.doc_ids = []

    def build(self, docs_jsonl):

        texts = []

        with open(docs_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                doc = json.loads(line)
                texts.append(doc["text"])
                self.doc_ids.append(doc["doc_id"])

        embeddings = self.model.encode(texts, show_progress_bar=True)

        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def save(self, path):

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, path + ".faiss")

        np.save(path + "_ids.npy", np.array(self.doc_ids))

    def load(self, path):

        self.index = faiss.read_index(path + ".faiss")
        self.doc_ids = np.load(path + "_ids.npy").tolist()

    def query(self, query, top_k=5):

        query_vec = self.model.encode([query]).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []

        for idx, score in zip(indices[0], distances[0]):
            results.append((self.doc_ids[idx], float(score)))

        return results
