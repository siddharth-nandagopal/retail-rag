from fastapi import APIRouter, HTTPException
import faiss
import numpy as np
import os
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from config.config import VECTOR_STORE_DIR
from model.load_model import ModelLoader
import psycopg2

from config.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


class InferenceRequest(BaseModel):
    query: str



router = APIRouter()

# Initialize the model loader
model_loader = ModelLoader()

product_index_file = os.path.join(VECTOR_STORE_DIR, 'faiss_product_index.bin')
financial_index_file = os.path.join(VECTOR_STORE_DIR, 'faiss_financial_index.bin')
time_index_file = os.path.join(VECTOR_STORE_DIR, 'faiss_time_index.bin')

product_index = None
financial_index = None
time_index = None

def load_indices():
    global product_index, financial_index, time_index
    if os.path.exists(product_index_file):
        product_index = faiss.read_index(product_index_file)
    if os.path.exists(financial_index_file):
        financial_index = faiss.read_index(financial_index_file)
    if os.path.exists(time_index_file):
        time_index = faiss.read_index(time_index_file)


def retrieve_similar_data_from_product_index(query_vector: list, k: int = 5):
    """
    Retrieve data similar to the query vector from the vector store.
    """
    if product_index is None:
        raise HTTPException(status_code=500, detail="FAISS product index not loaded")

    print(f"query_vector={query_vector}")

    # Perform a search in the vector store
    # distances, indices = product_index.search(np.array([query_vector], dtype='float32'), k)
    distances, indices = product_index.search(np.array(query_vector, dtype='float32'), k)
    print(f"distances={distances}")
    print(f"indices={indices}")
    
    # Retrieve and return the matched items (e.g., product descriptions)
    # In practice, one would map these indices back to actual product data from a database
    return {"indices": indices[0].tolist(), "distances": distances[0].tolist()}


load_indices()

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Function to retrieve product details from PostgreSQL using the indices
def get_product_details(indices):
    # Convert indices to a tuple for SQL IN clause
    index_tuple = tuple(indices)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT product_category, product_description, quantity, unit_price, price, discount_applied
        FROM retail_transactions
        WHERE invoice_id IN %s
        """,
        (index_tuple,)
    )
    return cursor.fetchall()

@router.post("/product_search")
async def search_product(request: InferenceRequest):
    try:
        query = request.query
        print(f"{query}")

        # Encode the query to a vector using the OpenAI API (or use a simple tokenizer if available)
        # query_embedding = model_loader.generate_response(query, max_tokens=100).encode('utf-8')[:384]
        # query_embedding = model_loader.generate_response(query, max_tokens=100).encode([query], convert_to_numpy=True)
        # Initialize the model for text embeddings
        model_name = 'all-MiniLM-L6-v2'  # Lightweight model for embedding generation
        model = SentenceTransformer(model_name)
        query_embedding = model.encode([query], convert_to_numpy=True)  # Convert to NumPy array
        print(f"query_embedding={query_embedding}")

        # Retrieve similar data from the vector store
        similar_data = retrieve_similar_data_from_product_index(query_embedding, k=5)
        print(f"similar_data={similar_data}")

        # Retrieve product details based on the indices
        product_details = get_product_details(similar_data['indices'])

        # Format the results for better readability
        results = [
            {
                "product_category": row[0],
                "product_description": row[1],
                "quantity_sold": row[2],
                "unit_price": row[3],
                "total_price": row[4],
                "discount_applied": row[5],
                "distance": similar_data['distances'][i]  # Include the distance for context
            }
            for i, row in enumerate(product_details)
        ]
        

        # Create a context from the similar data (for simplicity, use placeholder text)
        context = " ".join([f"Related data point {result}" for result in results])
        print(f"context={context}")

        # Generate a response using the OpenAI API with the retrieved context
        response = model_loader.generate_response(query, context=context)
        print(f"response={response}")

        return {"response": response, "related_data": similar_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/financial_search")
def search_financial(query_vector: list, k: int = 5):
    if not financial_index:
        raise HTTPException(status_code=500, detail="Financial FAISS index not loaded")

    query_embedding = np.array([query_vector], dtype='float32')
    distances, indices = financial_index.search(query_embedding, k)
    return {"distances": distances[0].tolist(), "indices": indices[0].tolist()}

@router.post("/time_search")
def search_time(query_vector: list, k: int = 5):
    if not time_index:
        raise HTTPException(status_code=500, detail="Time FAISS index not loaded")

    query_embedding = np.array([query_vector], dtype='float32')
    distances, indices = time_index.search(query_embedding, k)
    return {"distances": distances[0].tolist(), "indices": indices[0].tolist()}
