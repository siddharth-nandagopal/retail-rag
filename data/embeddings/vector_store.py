import os
import json
import faiss
import numpy as np

class VectorStore:
    def __init__(self, vector_store_dir='./vector_store_data', dimension=768):
        self.vector_store_dir = vector_store_dir
        self.dimension = dimension
        self.index_file = os.path.join(self.vector_store_dir, 'faiss_index.bin')
        self.index = None
        self.prompts_file = os.path.join(self.vector_store_dir, 'prompts.json')

        os.makedirs(self.vector_store_dir, exist_ok=True)
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            print("Loading existing FAISS index...")
            self.index = faiss.read_index(self.index_file)
            print("FAISS index loaded.")
        else:
            print("Creating new FAISS index...")
            self.index = faiss.IndexFlatL2(self.dimension)  # L2 distance index
            print("FAISS index created.")

    def add_embeddings(self, texts, embeddings):
        if len(embeddings) == 0:
            return

        embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
        print(f"Added {len(embeddings)} embeddings to the index.")
        self.save_index()

        with open(self.prompts_file, 'w') as f:
            json.dump(texts, f)

    def save_index(self):
        faiss.write_index(self.index, self.index_file)
        print(f"FAISS index saved to {self.index_file}")

    def search(self, query_embedding, k=5):
        query_embedding = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        return distances[0], indices[0]

    def load_prompts(self):
        if os.path.exists(self.prompts_file):
            with open(self.prompts_file, 'r') as f:
                return json.load(f)
        return []
