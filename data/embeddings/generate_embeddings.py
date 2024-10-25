import os
import json
import psycopg2
import numpy as np
import gc
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import StandardScaler
from vector_store import VectorStore
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, VECTOR_STORE_DIR
from datetime import datetime

# Load environment variables
# VECTOR_STORE_DIR = os.getenv('VECTOR_STORE_DIR', './vector_store_data')
PRODUCT_EMBEDDINGS_FILE = os.path.join(VECTOR_STORE_DIR, 'retail_transactions_product_embeddings.json')
FINANCIAL_EMBEDDINGS_FILE = os.path.join(VECTOR_STORE_DIR, 'retail_transactions_financial_embeddings.json')
TIME_EMBEDDINGS_FILE = os.path.join(VECTOR_STORE_DIR, 'retail_transactions_time_embeddings.json')

# Initialize the model for text embeddings
model_name = 'all-MiniLM-L6-v2'  # Lightweight model for embedding generation
model = SentenceTransformer(model_name)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Extract data from the `retail_transactions` table
def retrieve_data():
    print("Fetching data from the retail_transactions table...")
    cursor.execute("""
        SELECT product_category, product_description, quantity, unit_price, price, discount_applied, transaction_date
        FROM retail_transactions
    """)
    rows = cursor.fetchall()
    return rows

# Generate embeddings for product information
def generate_product_embeddings(rows):
    product_texts = [
        f"{row[0]} {row[1]}" for row in rows  # Combine `product_category` and `product_description`
    ]
    print("Generating embeddings for product information...")
    product_embeddings = model.encode(product_texts)
    print("Product embeddings generated.")

    # Save embeddings to JSON
    with open(PRODUCT_EMBEDDINGS_FILE, 'w') as f:
        json.dump({
            "product_texts": product_texts,
            "embeddings": product_embeddings.tolist()
        }, f)
    print(f"Product embeddings saved to {PRODUCT_EMBEDDINGS_FILE}")
    return product_texts, product_embeddings

# Generate normalized vectors for financial information
def generate_financial_embeddings(rows):
    financial_data = np.array([
        [row[2], row[3], row[4], row[5]]  # `quantity`, `unit_price`, `price`, `discount_applied`
        for row in rows
    ], dtype='float32')

    print("Normalizing financial data...")
    scaler = StandardScaler()
    financial_embeddings = scaler.fit_transform(financial_data)
    print("Financial embeddings generated and normalized.")

    # Save embeddings to JSON
    with open(FINANCIAL_EMBEDDINGS_FILE, 'w') as f:
        json.dump({
            "financial_data": financial_data.tolist(),
            "embeddings": financial_embeddings.tolist()
        }, f)
    print(f"Financial embeddings saved to {FINANCIAL_EMBEDDINGS_FILE}")
    return financial_embeddings

# Generate embeddings for time-based information
def generate_time_embeddings(rows):
    time_data = np.array([
        [datetime.timestamp(row[6])]  # Convert `transaction_date` to a timestamp
        for row in rows
    ], dtype='float32')

    print("Normalizing time data...")
    scaler = StandardScaler()
    time_embeddings = scaler.fit_transform(time_data)
    print("Time embeddings generated and normalized.")

    # Save embeddings to JSON
    with open(TIME_EMBEDDINGS_FILE, 'w') as f:
        json.dump({
            "time_data": time_data.tolist(),
            "embeddings": time_embeddings.tolist()
        }, f)
    print(f"Time embeddings saved to {TIME_EMBEDDINGS_FILE}")
    return time_embeddings

# Store embeddings in the vector store
def store_embeddings(texts, product_embeddings, financial_embeddings, time_embeddings):
    vector_store = VectorStore(VECTOR_STORE_DIR)

    # Store product-related embeddings
    vector_store.add_embeddings(texts, product_embeddings)
    print("Product embeddings added to vector store.")

    # Store financial embeddings (can be stored in a separate index or combined)
    vector_store.add_embeddings(
        ["financial_vector"] * len(financial_embeddings),
        financial_embeddings
    )
    print("Financial embeddings added to vector store.")

    # Store time-based embeddings
    vector_store.add_embeddings(
        ["time_vector"] * len(time_embeddings),
        time_embeddings
    )
    print("Time embeddings added to vector store.")

# Main function
def main():
    rows = retrieve_data()
    product_texts, product_embeddings = generate_product_embeddings(rows)
    financial_embeddings = generate_financial_embeddings(rows)
    time_embeddings = generate_time_embeddings(rows)
    store_embeddings(product_texts, product_embeddings, financial_embeddings, time_embeddings)

    # Close the database connection
    cursor.close()
    conn.close()
    print("All embeddings generated and stored successfully.")

if __name__ == "__main__":
    main()
