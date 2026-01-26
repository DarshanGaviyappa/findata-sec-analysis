"""DAG 3: Fact Tables Pipeline"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {"owner": "findata_team", "start_date": datetime(2024, 1, 1)}

def create_fact_tables():
    print("Creating denormalized fact tables...")

with DAG("fact_tables_pipeline", default_args=default_args, schedule_interval="@quarterly") as dag:
    create = PythonOperator(task_id="create_facts", python_callable=create_fact_tables)

