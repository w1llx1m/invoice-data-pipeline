DROP TABLE IF EXISTS invoices;

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    city VARCHAR(100),
    email VARCHAR(255),
    amount NUMERIC(10, 2),
    quantity INTEGER,
    invoice_date DATE,
    address VARCHAR(255),
    job VARCHAR(150),
    created_at TIMESTAMP DEFAULT NOW()
);