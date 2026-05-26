import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import psycopg2

# Centralized environment variable management with safe fallbacks
DB_HOST = os.getenv("DB_HOST") or "postgres"
DB_NAME = os.getenv("DB_NAME") or "airflow_metadata"
DB_USER = os.getenv("DB_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "Oracle22$"

def create_bronze_lakehouse_layer():
    """Simulates a lakehouse Bronze tier landing zone inside the warehouse."""
    conn = psycopg2.connect(
        host=DB_HOST, 
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    curr = conn.cursor()
    
    # Build out clean target schemas
    curr.execute("CREATE SCHEMA IF NOT EXISTS lakehouse_bronze;")
    
    # Extract data directly from raw source tables into lakehouse landing tier
    # NOTE: Replaced "AS SELECT * ... ON CONFLICT" with a robust drop/create cycle to allow clean pipeline retries
    curr.execute("DROP TABLE IF EXISTS lakehouse_bronze.customers;")
    curr.execute("""
        CREATE TABLE lakehouse_bronze.customers AS 
        SELECT * FROM raw_source.customers;
    """)
    
    curr.execute("DROP TABLE IF EXISTS lakehouse_bronze.orders;")
    curr.execute("""
        CREATE TABLE lakehouse_bronze.orders AS 
        SELECT * FROM raw_source.orders;
    """)
    
    conn.commit()
    curr.close()
    conn.close()
    print("--- Bronze Tier Infrastructure Initialized ---")

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'ecommerce_lakehouse_pipeline',
    default_args=default_args,
    description='End-to-End E-Commerce Medallion Architecture Batch Pipeline',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Task 1: Generate Mock Data inside raw_source schema
    task_generate_source_data = BashOperator(
        task_id='generate_source_data',
        bash_command='python /opt/airflow/scripts/generate_mock_data.py',
    )

    # Task 2: Load to Bronze Tier Lakehouse table
    task_load_to_bronze = PythonOperator(
        task_id='load_to_bronze_lakehouse',
        python_callable=create_bronze_lakehouse_layer,
    )

    # Task 3: Transform to Gold Tier analytics marts (Escaped password syntax for Bash)
    task_transform_silver_gold = BashOperator(
        task_id='transform_silver_gold_marts',
        bash_command='''psql postgresql://postgres:Oracle22\\$@postgres:5432/airflow_metadata -c "
        CREATE SCHEMA IF NOT EXISTS lakehouse_gold;
        DROP TABLE IF EXISTS lakehouse_gold.fact_customer_revenue_marts;
        CREATE TABLE lakehouse_gold.fact_customer_revenue_marts AS
        SELECT 
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) as full_name,
            c.email,
            SUM(o.order_amount) as total_revenue_spent,
            COUNT(o.order_id) as total_orders_placed
        FROM raw_source.customers c
        JOIN raw_source.orders o ON c.customer_id = o.customer_id
        WHERE o.order_status = 'COMPLETED'
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email;
        "'''
    )

    task_generate_source_data >> task_load_to_bronze >> task_transform_silver_gold