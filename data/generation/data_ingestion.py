import os
import psycopg2
import csv
from faker import Faker
import random
from datetime import datetime, timedelta
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, CUSTOMER_CSV, PRODUCT_CSV, STORE_CSV, TRANSACTION_CSV, REVIEW_CSV

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Initialize Faker for realistic data generation
fake = Faker()

# Function to write data to a CSV file incrementally
def write_to_csv(file_path, num_rows, generator_func, header):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in generator_func(num_rows):
            writer.writerow(row)
    print(f"Data written to {file_path}")

# Data generator functions
def generate_customers(num_customers=10000):
    for customer_id in range(1, num_customers + 1):
        yield (
            customer_id,
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.address(),
            fake.country(),
            fake.state(),
            fake.city(),
            fake.date_time_this_decade()
        )

def generate_products(num_products=500):
    for product_id in range(1, num_products + 1):
        category = fake.random_element(elements=("Electronics", "Clothing", "Groceries", "Home & Kitchen", "Sports"))
        yield (
            product_id,
            fake.word().capitalize() + " " + category,
            category,
            fake.sentence(nb_words=12),
            round(random.uniform(5, 500), 2),
            fake.date_time_this_decade()
        )

def generate_stores(num_stores=100):
    for store_id in range(1, num_stores + 1):
        yield (
            store_id,
            "Store " + str(store_id),
            fake.street_address(),
            fake.country(),
            fake.state(),
            fake.city(),
            fake.date_time_this_decade()
        )

def generate_transactions(num_transactions=1000000, num_customers=10000, num_products=500):
    for _ in range(num_transactions):
        invoice_id = random.randint(100000, 999999)
        customer_id = random.randint(1, num_customers)
        product_id = random.randint(1, num_products)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(5, 500), 2)
        discount = round(random.uniform(0, 0.3), 2)
        price = unit_price * quantity * (1 - discount)
        transaction_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
        payment_method = random.choice(["cash", "credit card", "paypal", "debit card"])
        card_type = random.choice(["visa", "master card", "amex"]) if payment_method == "credit card" else None
        yield (
            invoice_id, customer_id, product_id, quantity, unit_price, price, discount * 100,
            transaction_date, payment_method, card_type,
            fake.street_address(), fake.country(), fake.state(), fake.city(),
            fake.random_element(elements=("Electronics", "Clothing", "Groceries", "Home & Kitchen", "Sports")),
            fake.sentence(nb_words=8), round(price, 2), round(price * quantity, 2)
        )

def generate_reviews(num_reviews=100000, num_customers=10000, num_products=500):
    for review_id in range(1, num_reviews+1):
        customer_id = random.randint(1, num_customers)
        product_id = random.randint(1, num_products)
        rating = random.randint(1, 5)  # Ensure rating is an integer between 1 and 5
        review_text = fake.sentence(nb_words=15)  # Generate a textual review
        review_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
        yield (
            review_id,
            customer_id,
            product_id,
            rating,
            review_text,
            review_date
        )

# Function to load data from CSV into PostgreSQL using COPY
def load_csv_to_postgresql(file_path, table_name):
    with open(file_path, 'r') as f:
        next(f)  # Skip the header row
        # Clear existing data from the table
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", f)
    conn.commit()
    print(f"Data loaded into table '{table_name}' successfully.")

# Paths for CSV files
csv_files = {
    "customer_details": "customer_details.csv",
    "product_details": "product_details.csv",
    "store_details": "store_details.csv",
    "retail_transactions": "retail_transactions.csv",
    "customer_reviews": "customer_reviews.csv"
}

# Write data to CSV files and load into PostgreSQL
write_to_csv(csv_files["customer_details"], 10000, generate_customers, [
    'customer_id', 'customer_name', 'email', 'phone', 'address', 'country', 'state', 'city', 'created_at'
])
load_csv_to_postgresql(csv_files["customer_details"], 'customer_details')

write_to_csv(csv_files["product_details"], 500, generate_products, [
    'product_id', 'product_name', 'product_category', 'product_description', 'unit_price', 'created_at'
])
load_csv_to_postgresql(csv_files["product_details"], 'product_details')

write_to_csv(csv_files["store_details"], 100, generate_stores, [
    'store_id', 'store_name', 'store_address', 'store_country', 'store_state', 'store_city', 'created_at'
])
load_csv_to_postgresql(csv_files["store_details"], 'store_details')

write_to_csv(csv_files["retail_transactions"], 1000000, generate_transactions, [
    'invoice_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'price', 'discount_applied',
    'transaction_date', 'payment_method', 'card_type', 'store_address', 'store_country', 'store_state',
    'store_city', 'product_category', 'product_description', 'product_total_amount', 'transaction_total_amount'
])
load_csv_to_postgresql(csv_files["retail_transactions"], 'retail_transactions')

write_to_csv(csv_files["customer_reviews"], 100000, generate_reviews, [
    'customer_id', 'product_id', 'rating', 'review_text', 'review_date'
])
load_csv_to_postgresql(csv_files["customer_reviews"], 'customer_reviews')

# Clean up CSV files
for file in csv_files.values():
    os.remove(file)
    print(f"Removed {file}")

# Close the connection
cursor.close()
conn.close()