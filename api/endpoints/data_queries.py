from fastapi import APIRouter, HTTPException
import psycopg2

from config.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

router = APIRouter()


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

@router.get("/customers/{customer_id}")
def get_customer_details(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_details WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    conn.close()

    if customer:
        return {"customer": customer}
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@router.get("/products/{product_id}")
def get_product_details(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_details WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return {"product": product}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
