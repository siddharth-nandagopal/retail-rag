import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the root of the project
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Database connection configuration from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Paths for data generation
GENERATED_DATA_DIR = os.getenv('GENERATED_DATA_DIR')
CUSTOMER_CSV = os.path.join(GENERATED_DATA_DIR, 'customer_details.csv')
PRODUCT_CSV = os.path.join(GENERATED_DATA_DIR, 'product_details.csv')
STORE_CSV = os.path.join(GENERATED_DATA_DIR, 'store_details.csv')
TRANSACTION_CSV = os.path.join(GENERATED_DATA_DIR, 'retail_transactions.csv')
REVIEW_CSV = os.path.join(GENERATED_DATA_DIR, 'customer_reviews.csv')
