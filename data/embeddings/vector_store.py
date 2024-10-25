import os
import json
import faiss
import numpy as np

class VectorStore:
    def __init__(self, vector_store_dir='./vector_store_data'):
        self.vector_store_dir = vector_store_dir
        self.product_index_file = os.path.join(self.vector_store_dir, 'faiss_product_index.bin')
        self.financial_index_file = os.path.join(self.vector_store_dir, 'faiss_financial_index.bin')
        self.time_index_file = os.path.join(self.vector_store_dir, 'faiss_time_index.bin')
        self.product_index = None
        self.financial_index = None
        self.time_index = None

        os.makedirs(self.vector_store_dir, exist_ok=True)
        self._load_indices()

    def _load_indices(self):
        self.product_index = self._load_index(self.product_index_file, 384, "product")
        self.financial_index = self._load_index(self.financial_index_file, 4, "financial")
        self.time_index = self._load_index(self.time_index_file, 1, "time")

    def _load_index(self, index_file, dimension, index_type):
        if os.path.exists(index_file):
            print(f"Loading existing {index_type} FAISS index...")
            index = faiss.read_index(index_file)
            print(f"{index_type.capitalize()} FAISS index loaded.")
        else:
            print(f"Creating new {index_type} FAISS index with dimension {dimension}...")
            index = faiss.IndexFlatL2(dimension)
            print(f"{index_type.capitalize()} FAISS index created.")
        return index

    def add_embeddings(self, index_type, texts, embeddings):
        """
        Add new embeddings to the vector store.
        """
        if len(embeddings) == 0:
            return

        # Ensure that embeddings have the correct dimension
        embeddings = np.array(embeddings).astype('float32')
        if index_type == "product":
            self.index = self.product_index
            self.index_file = self.product_index_file
        elif index_type == "financial":
            self.index = self.financial_index
            self.index_file = self.financial_index_file
        elif index_type == "time":
            self.index = self.time_index
            self.index_file = self.time_index_file
        else:
            raise ValueError(f"Invalid index type: {index_type}")
        
        if embeddings.shape[1] != self.index.d:
            raise ValueError(
                f"Embedding dimension {embeddings.shape[1]} does not match FAISS index dimension {self.index.d} for {index_type}"
            )

        # Add embeddings to the index
        self.index.add(embeddings)
        print(f"Added {len(embeddings)} {index_type} embeddings to the index.")
        self.save_index(self.index, self.index_file)

        # Save texts for reference (if applicable)
        if texts:
            with open(self.index_file.replace('.bin', '_texts.json'), 'a') as f:
                json.dump(texts, f)

    def save_index(self, index, index_file):
        """
        Save the FAISS index to disk.
        """
        faiss.write_index(index, index_file)
        print(f"FAISS index saved to {index_file}")

    def search(self, index_type, query_embedding, k=5):
        """
        Search for the top-k similar embeddings.
        """
        query_embedding = np.array([query_embedding]).astype('float32')
        if index_type == "product":
            index = self.product_index
        elif index_type == "financial":
            index = self.financial_index
        elif index_type == "time":
            index = self.time_index
        else:
            raise ValueError(f"Invalid index type: {index_type}")

        distances, indices = index.search(query_embedding, k)
        return distances[0], indices[0]

    def load_prompts(self):
        if os.path.exists(self.prompts_file):
            with open(self.prompts_file, 'r') as f:
                return json.load(f)
        return []
