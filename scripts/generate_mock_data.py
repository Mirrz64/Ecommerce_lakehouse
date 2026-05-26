import os
import random
import psycopg2
from datetime import datetime

# Fetch from environment; if blank, fall back safely to the default network values
DB_HOST = os.getenv("DB_HOST") or "postgres"
DB_NAME = os.getenv("DB_NAME") or "airflow_metadata"
DB_USER = os.getenv("DB_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "postgres_secure_pwd"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, 
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )

def init_source_tables():
    commands = (
        """
        CREATE SCHEMA IF NOT EXISTS raw_source;
        """,
        """
        CREATE TABLE IF NOT EXISTS raw_source.customers (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw_source.orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES raw_source.customers(customer_id),
            order_amount DECIMAL(10, 2),
            order_status VARCHAR(20),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn = get_connection()
    curr = conn.cursor()
    for command in commands:
        curr.execute(command)
    conn.commit()
    curr.close()
    conn.close()

def populate_mock_data():
    conn = get_connection()
    curr = conn.cursor()
    
    # Generate 5 unique customers
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam"]
    last_names = ["Smith", "Jones", "Miller", "Davis", "Wilson"]
    
    for i in range(5):
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        email = f"{f_name.lower()}.{l_name.lower()}{random.randint(1,99)}@example.com"
        
        try:
            curr.execute(
                "INSERT INTO raw_source.customers (first_name, last_name, email) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING;",
                (f_name, l_name, email)
            )
        except psycopg2.Error as e:
            print(f"Skipping duplicate customer: {e}")
            conn.rollback()
            
    conn.commit()
    
    # Grab valid customer IDs to map orders correctly
    curr.execute("SELECT customer_id FROM raw_source.customers;")
    customer_ids = [row[0] for row in curr.fetchall()]
    
    if customer_ids:
        for _ in range(10):
            cust_id = random.choice(customer_ids)
            amount = round(random.uniform(10.50, 250.75), 2)
            status = random.choice(["COMPLETED", "PENDING", "CANCELLED"])
            curr.execute(
                "INSERT INTO raw_source.orders (customer_id, order_amount, order_status) VALUES (%s, %s, %s);",
                (cust_id, amount, status)
            )
        conn.commit()
        
    curr.close()
    conn.close()
    print("--- Mock Data Ingestion Completed Successfully ---")

if __name__ == "__main__":
    init_source_tables()
    populate_mock_data()