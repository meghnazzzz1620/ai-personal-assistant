import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Dimension of embeddings (MiniLM gives 384)
        self.dimension = 384
        
        # FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store mapping of vector position → text
        self.text_store = []

    def add_text(self, text: str):
        embedding = self.model.encode([text])
        embedding = np.array(embedding).astype("float32")
        
        self.index.add(embedding)
        self.text_store.append(text)

   


    def search(self, query: str, top_k: int = 6):

        if self.index.ntotal == 0:
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue

            if 0 <= idx < len(self.text_store):
                candidate = self.text_store[idx]

            # Ignore exact same query
                if candidate.strip().lower() == query.strip().lower():
                    continue

                results.append(candidate)

        return results

   

    
