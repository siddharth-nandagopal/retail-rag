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

# Generator function to fetch data in chunks
def fetch_data_in_batches(batch_size=1000):
    cursor.execute("""
        SELECT product_category, product_description, quantity, unit_price, price, discount_applied, transaction_date 
        FROM retail_transactions
        LIMIT 2000
    """)
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

# Generate and store embeddings for each batch
def process_and_store_embeddings(batch_size=1000):
    scaler = StandardScaler()

    for batch_idx, rows in enumerate(fetch_data_in_batches(batch_size=batch_size)):
        # Prepare product-related text data
        product_texts = [f"{row[0]} {row[1]}" for row in rows]

        # Generate product embeddings in batches
        print(f"Generating product embeddings for batch {batch_idx}...")
        product_embeddings = model.encode(product_texts, batch_size=32, convert_to_numpy=True)
        print(f"Product embeddings for batch {batch_idx} generated.")

        # Process financial data and normalize
        financial_data = np.array(
            [[row[2], row[3], row[4], row[5]] for row in rows], dtype='float32'
        )
        financial_embeddings = scaler.fit_transform(financial_data)
        print(f"Financial embeddings for batch {batch_idx} generated and normalized.")

        # Process time data and normalize
        time_data = np.array(
            [[datetime.timestamp(row[6])] for row in rows], dtype='float32'
        )
        time_embeddings = scaler.fit_transform(time_data)
        print(f"Time embeddings for batch {batch_idx} generated and normalized.")

        # Save and store the embeddings for this batch
        save_embeddings(batch_idx, product_texts, product_embeddings, financial_embeddings, time_embeddings)
        print(f"Embeddings for batch {batch_idx} saved.")

        # Perform garbage collection to free memory
        del product_embeddings, financial_embeddings, time_embeddings, product_texts
        gc.collect()

# Save embeddings to JSON and add to vector store
def save_embeddings(batch_idx, product_texts, product_embeddings, financial_embeddings, time_embeddings):
    # Create vector store instance
    vector_store = VectorStore(VECTOR_STORE_DIR)

    # Store product-related embeddings in the product index
    vector_store.add_embeddings("product", product_texts, product_embeddings)
    print(f"Product embeddings for batch {batch_idx} added to vector store.")

    # Store financial embeddings in the financial index
    vector_store.add_embeddings("financial", ["financial_vector"] * len(financial_embeddings), financial_embeddings)
    print(f"Financial embeddings for batch {batch_idx} added to vector store.")

    # Store time-based embeddings in the time index
    vector_store.add_embeddings("time", ["time_vector"] * len(time_embeddings), time_embeddings)
    print(f"Time embeddings for batch {batch_idx} added to vector store.")

    # Save embeddings to JSON files for reference
    with open(PRODUCT_EMBEDDINGS_FILE.replace('.json', f'_{batch_idx}.json'), 'w') as f:
        json.dump({"product_texts": product_texts, "embeddings": product_embeddings.tolist()}, f)
    with open(FINANCIAL_EMBEDDINGS_FILE.replace('.json', f'_{batch_idx}.json'), 'w') as f:
        json.dump({"financial_data": financial_embeddings.tolist()}, f)
    with open(TIME_EMBEDDINGS_FILE.replace('.json', f'_{batch_idx}.json'), 'w') as f:
        json.dump({"time_data": time_embeddings.tolist()}, f)


# Main function to process all data in batches
def main():
    process_and_store_embeddings(batch_size=1000)
    cursor.close()
    conn.close()
    print("All embeddings generated and stored successfully.")

if __name__ == "__main__":
    main()