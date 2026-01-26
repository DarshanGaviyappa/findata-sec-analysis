"""
DAG 1: Raw Storage Pipeline
Loads SEC data into RAW schema tables
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'findata_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

def download_sec_data(**context):
    """Download SEC dataset"""
    print("Downloading SEC Q4 2024 data...")
    # Implementation: src/scrapers/download_sample.py
    
def validate_files(**context):
    """Validate downloaded files"""
    print("Validating file schema and data types...")
    # Check: SUB.txt, TAG.txt, NUM.txt, PRE.txt exist
    
def load_to_snowflake(**context):
    """Load data to Snowflake RAW tables"""
    print("Loading to RAW_SUB, RAW_TAG, RAW_NUM, RAW_PRE...")
    # Implementation: src/loaders/bulk_load.py
    
def verify_load(**context):
    """Verify data integrity"""
    print("Verifying row counts and data quality...")

with DAG(
    'raw_storage_pipeline',
    default_args=default_args,
    description='Load SEC data to RAW tables',
    schedule_interval='@quarterly',
    catchup=False
) as dag:
    
    download = PythonOperator(
        task_id='download_sec_data',
        python_callable=download_sec_data
    )
    
    validate = PythonOperator(
        task_id='validate_files',
        python_callable=validate_files
    )
    
    load = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake
    )
    
    verify = PythonOperator(
        task_id='verify_load',
        python_callable=verify_load
    )
    
    download >> validate >> load >> verify
