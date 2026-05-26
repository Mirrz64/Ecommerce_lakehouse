from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# 1. Baseline configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# 2. Instantiate DAG
with DAG(
    dag_id='ecommerce_lakehouse_pipeline',
    default_args=default_args,
    description='End-to-End E-Commerce Medallion Architecture Batch Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['ecommerce', 'dbt', 'lakehouse'],
) as dag:

    # Task 1: Generate the source rows
    generate_source_data = BashOperator(
        task_id='generate_source_data',
        bash_command='python /opt/airflow/scripts/generate_mock_data.py',
    )

    # Task 2: Mock ingest tool step to load into raw/bronze database layers
    load_to_bronze_lakehouse = BashOperator(
        task_id='load_to_bronze_lakehouse',
        bash_command='echo "Loading operational data warehouse data into landing layers..."',
    )

    # Task 3: Build the dbt transformation layer models (Silver / Gold)
    transform_silver_gold_marts = BashOperator(
        task_id='transform_silver_gold_marts',
        bash_command='cd /opt/airflow/dbt_project && dbt run',
    )

    # 👇 Task 4: The new Automated Testing Step 👇
    run_dbt_tests = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd /opt/airflow/dbt_project && dbt test',
    )

    # 3. Execution Flow Chain (Matches your UI layout flawlessly!)
    generate_source_data >> load_to_bronze_lakehouse >> transform_silver_gold_marts >> run_dbt_tests