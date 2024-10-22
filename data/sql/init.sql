DROP TABLE IF EXISTS retail_transactions;
CREATE TABLE retail_transactions (
    invoice_id INT,
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price FLOAT,
    price FLOAT,
    discount_applied FLOAT,
    transaction_date TIMESTAMPTZ,
    payment_method VARCHAR(20),
    card_type VARCHAR(20),
    store_address VARCHAR(100),
    store_country VARCHAR(100),
    store_state VARCHAR(50),
    store_city VARCHAR(50),
    product_category VARCHAR(50),
    product_description TEXT,
    product_total_amount FLOAT,
    transaction_total_amount FLOAT
);

DROP TABLE IF EXISTS customer_details;
CREATE TABLE customer_details (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address VARCHAR(150),
    country VARCHAR(100),
    state VARCHAR(50),
    city VARCHAR(50),
    created_at TIMESTAMPTZ
);

DROP TABLE IF EXISTS product_details;
CREATE TABLE product_details (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_category VARCHAR(50),
    product_description TEXT,
    unit_price FLOAT,
    created_at TIMESTAMPTZ
);

DROP TABLE IF EXISTS store_details;
CREATE TABLE store_details (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    store_address VARCHAR(100),
    store_country VARCHAR(100),
    store_state VARCHAR(50),
    store_city VARCHAR(50),
    created_at TIMESTAMPTZ
);

DROP TABLE IF EXISTS customer_reviews;
CREATE TABLE customer_reviews (
    review_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    rating INT,
    review_text TEXT,
    review_date TIMESTAMPTZ,
    FOREIGN KEY (customer_id) REFERENCES customer_details(customer_id),
    FOREIGN KEY (product_id) REFERENCES product_details(product_id)
);