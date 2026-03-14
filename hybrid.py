import numpy as np
from app.search.bm25 import BM25Index
from app.search.vector import VectorIndex


class HybridSearch:

    def __init__(self, bm25_path, vector_path):

        self.bm25 = BM25Index()
        self.vector = VectorIndex()

        self.bm25.load(bm25_path)
        self.vector.load(vector_path)

    def normalize(self, scores):

        scores = np.array(scores)

        if scores.max() == scores.min():
            return np.zeros_like(scores)

        return (scores - scores.min()) / (scores.max() - scores.min())

    def search(self, query, top_k=5, alpha=0.5):

        bm25_results = self.bm25.query(query, top_k=top_k*2)
        vector_results = self.vector.query(query, top_k=top_k*2)

        bm25_dict = {doc:score for doc,score in bm25_results}
        vector_dict = {doc:score for doc,score in vector_results}

        all_docs = set(bm25_dict.keys()) | set(vector_dict.keys())

        bm25_scores = []
        vector_scores = []

        doc_list = list(all_docs)

        for doc in doc_list:
            bm25_scores.append(bm25_dict.get(doc,0))
            vector_scores.append(vector_dict.get(doc,0))

        bm25_scores = self.normalize(bm25_scores)
        vector_scores = self.normalize(vector_scores)

        hybrid_scores = alpha * bm25_scores + (1-alpha) * vector_scores

        results = list(zip(doc_list, hybrid_scores))

       

        results.sort(key=lambda x: x[1], reverse=True)

        threshold = 0.3
        filtered = []

        for doc_id, hybrid_score in results:

            bm25_score = bm25_dict.get(doc_id, 0)

            combined_score = hybrid_score + bm25_score

        if combined_score >= threshold:
            filtered.append((doc_id, hybrid_score))

        return filtered[:top_k]
